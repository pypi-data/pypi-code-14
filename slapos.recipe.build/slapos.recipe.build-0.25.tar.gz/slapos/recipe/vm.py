##############################################################################
#
# Copyright (c) 2016 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

import base64, os, select, shutil, socket
import subprocess, sys, tempfile, threading, time
from contextlib import contextmanager
from os.path import join
from slapos.recipe import EnvironMixin, generatePassword, logger, rmtree
from zc.buildout import UserError

ARCH = os.uname()[4]

@contextmanager
def building_directory(directory):
  if os.path.lexists(directory):
    logger.warning('Removing already existing path %r', directory)
    rmtree(directory)
  os.makedirs(directory)
  try:
    yield
  except:
    shutil.rmtree(directory)
    raise


class Popen(subprocess.Popen):

  def stop(self):
    if self.pid and self.returncode is None:
      self.terminate()
      t = threading.Timer(5, self.kill)
      t.start()
      # PY3: use waitid(WNOWAIT) and call self.poll() after t.cancel()
      r = self.wait()
      t.cancel()
      return r


class BaseRecipe(EnvironMixin):

  def __init__(self, buildout, name, options, allow_none=True):
    self.buildout = buildout
    self.options = options
    try:
      options['location'] = options['location'].strip()
    except KeyError:
      options['location'] = join(buildout['buildout']['parts-directory'], name)
    EnvironMixin.__init__(self, allow_none)

  def getQemuBasicArgs(self, dist, mem=None, snapshot=False,
                             unsafe=False, ssh=None):
    drive = 'file=%s/%s.img,format=raw,discard=on' % (self.vm, dist)
    if snapshot:
      drive += ',snapshot=on'
    elif unsafe:
      drive += ',cache=unsafe'
    net = 'user'
    if ssh:
      net += ',hostfwd=tcp:127.0.0.1:%s-:22' % ssh
    try:
      mem = eval(self.options['mem'], {})
    except KeyError:
      if mem is None:
        raise
    return ['qemu-system-' + ARCH, '-enable-kvm', '-drive', drive,
            '-smp', self.options.get('smp', '1'), '-m', str(mem),
            '-net', 'nic,model=virtio', '-net', net]

  @property
  def ssh_key(self):
    return join(self.vm, 'ssh.key')

  def update(self):
    pass


class InstallDebianRecipe(BaseRecipe):

  preseed = """
    auto = true
    priority = critical
    partman/choose_partition = finish
    partman-basicfilesystems/no_swap = false
    partman/confirm = true
    partman/confirm_nooverwrite = true
    grub-installer/bootdev = default
    finish-install/reboot_in_progress = note
    preseed/url = file:///dev/null

    clock-setup/ntp = false
    time/zone = UTC
    language = C
    country = FR
    keymap = us
    passwd/make-user = false
    partman-auto/method = regular
    partman-auto/expert_recipe = : 1 1 -1 ext4 $primary{ } $bootable{ } method{ format } format{ } use_filesystem{ } filesystem{ ext4 } mountpoint{ / } options/discard{ } options/noatime{ } .
    """

  def __init__(self, buildout, name, options):
    BaseRecipe.__init__(self, buildout, name, options)
    self.vm = options['location']
    self.dists = dists = []
    arch = options.get('arch') or ARCH
    for name in options['dists'].split():
      dist = buildout[name]
      iso = buildout[dist[arch + '.iso']]
      dists.append((name,
        join(iso['location'], iso['filename']),
        dist[arch + '.kernel'],
        dist[arch + '.initrd']))

    if 'preseed.preseed/late_command' in options:
      raise UserError("use 'late-command' recipe option instead")
    late_command = (options.get('late-command') or '').strip()
    self.late_command = [late_command] if late_command else []

    size = options['size'].strip()
    i = -2 if size[-1] == 'i' else -1
    try:
      size = (1024, 1000)[i] ** ' kMGTP'.index(size[i]) * eval(size[:i])
    except ValueError:
      self.size = eval(size)
    else:
      self.size = (1 + int(size / 512)) * 512 if size % 512 else int(size)

  def install(self):
    options = self.options
    cmdline = {}
    for preseed in self.preseed.splitlines():
      preseed = preseed.strip()
      if preseed:
        k, v = preseed.split('=', 1)
        cmdline[k.strip()] = v.strip()
    for k, v in options.iteritems():
      if k.startswith('preseed.'):
        cmdline[k[8:]] = v.strip()
      elif k.startswith('debconf.'):
        owner = k[8:] + ':'
        for k in v.splitlines():
          try:
            k, v = k.split(None, 1)
          except ValueError:
            if not k:
              continue
            v = ''
          cmdline[owner + k] = v
    packages = options.get('packages', 'ssh').split()
    if packages:
      cmdline['pkgsel/include'] = ','.join(packages)
    if 'passwd/root-password' in cmdline:
      root_password = None
    else:
      cmdline['passwd/root-password'] = root_password = \
      cmdline['passwd/root-password-again'] = generatePassword()
    env = self.environ

    location = self.vm
    with building_directory(location):
      if 'ssh' in packages:
        key = self.ssh_key
        subprocess.check_call(('ssh-keygen', '-N', '', '-f', key), env=env)
        key += '.pub'
        with open(key) as f:
          os.remove(key)
          key = f.read().strip()
        self.late_command.append(
          "mkdir -m 0700 ~/.ssh && echo %s > ~/.ssh/authorized_keys" % key)
      if self.late_command:
        cmdline['preseed/late_command'] = (
          'cd /target && echo %s|usr/bin/base64 -d|chroot . sh'
          % base64.standard_b64encode(
            'export HOME=/root\n' + '\n'.join(self.late_command)))

      for dist, iso, kernel, initrd in self.dists:
        vm = join(location, dist + '.img')
        args = self.getQemuBasicArgs(dist, 256, unsafe=True)
        open_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_TRUNC
        fd = os.open(vm, open_flags, 0666)
        try:
          os.ftruncate(fd, self.size)
        finally:
          os.close(fd)
        tmp = tempfile.mkdtemp()
        try:
          subprocess.check_call(('7z', 'x', iso, kernel, initrd),
                                cwd=tmp, env=env)
          args += (
            '-vnc', join('unix:' + tmp, 'vnc.sock'), # for debugging purpose
            '-cdrom', iso, '-no-reboot',
            '-kernel', join(tmp, kernel),
            '-initrd', join(tmp, initrd),
            '-append', ' '.join(k + '=' + ('"' + v + '"' if ' ' in v else v)
                                for k, v in cmdline.iteritems()))
          subprocess.check_call(args, env=env)
        finally:
          shutil.rmtree(tmp)
        if not subprocess.check_output(('file', '-b', vm), env=env).startswith(
            'DOS/MBR boot sector'):
          raise Exception('non bootable image')

      if root_password:
        fd = os.open(join(location, 'passwd'), open_flags, 0600)
        try:
          os.write(fd, "root:%s\n" % root_password)
        finally:
          os.close(fd)

    return [location]


class RunRecipe(BaseRecipe):

  command = """set -e
reboot() {
  unset -f reboot
  %s
  (while pgrep -x sshd; do sleep 1; done >/dev/null; reboot
  ) >/dev/null 2>&1 &
  exit
}
map() {
  local x=${1#%s}; case $x in $1) exit 1;; ''|/*) ;; *) exit 1;; esac
  echo /mnt/buildout$x
}
PARTDIR=`map %s`
(cd /mnt; set %s; mkdir -p $*; for tag; do
   mount -t 9p -o trans=virtio,version=9p2000.L,noatime $tag $tag
 done)
"""

  def __init__(self, buildout, name, options):
    BaseRecipe.__init__(self, buildout, name, options, False)
    self.vm = options['vm']
    self.mount_dict = {'buildout': buildout['buildout']['directory']}
    for k, v in options.iteritems():
      if k == 'mount.buildout':
        raise UserError('option %r can not be overridden' % k)
      v = v.strip()
      if k.startswith('mount.') and v:
        self.mount_dict[k[6:]] = v

  def install(self):
    env = self.environ
    options = self.options
    location = options['location']
    mount_args = []
    for i, (tag, path) in enumerate(self.mount_dict.iteritems()):
      mount_args += (
        '-fsdev', 'local,security_model=none,id=fsdev%s,path=%s'
          % (i, path),
        '-device', 'virtio-9p-pci,id=fs%s,fsdev=fsdev%s,mount_tag=%s'
          % (i, i, tag))
    init = self.command % (
      options.get('stop-ssh', 'systemctl stop ssh'),
      self.buildout['buildout']['directory'],
      location, ' '.join(self.mount_dict))
    commands = map(options.__getitem__,
      options.get('commands', 'command').split())
    hostfwd_retries = 9
    wait_ssh = int(options.get('wait-ssh') or 60)
    with building_directory(location):
      tmp = tempfile.mkdtemp()
      try:
        vnc = join(tmp, 'vnc.sock')
        # Unfortunately, QEMU can't redirect from host socket to guest TCP (SSH
        # does it), so we try a random port until QEMU is able to listen to it.
        # In order to speed up the process, we request free ports from the
        # kernel, but we still have to retry in case of race condition.
        # We assume that QEMU sets up host redirection before creating the VNC
        # socket path.
        while 1:
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.bind(('127.0.0.1', 0))
          ssh = s.getsockname()
          args = self.getQemuBasicArgs(
            options['dist'], snapshot=True, ssh=ssh[1]) + [
            '-vnc', 'unix:' + vnc] + mount_args
          s.close()
          p = Popen(args, stderr=subprocess.PIPE, env=dict(env,
            TMPDIR=location, # for snapshot
            ))
          try:
            while not select.select((p.stderr,), (), (), 1)[0]:
              if os.path.exists(vnc):
                break
            else:
              err = p.communicate()[1]
              sys.stderr.write(err)
              if ('could not set up host forwarding rule' in err and
                  hostfwd_retries):
                hostfwd_retries -= 1
                continue
              raise subprocess.CalledProcessError(p.returncode, args)
            for command in commands:
              timeout = time.time() + wait_ssh
              while 1:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(ssh)
                if s.recv(4) == 'SSH-':
                  break
                s.close()
                if time.time() >= timeout:
                  raise Exception("Can not SSH to VM after %s seconds"
                                  % wait_ssh)
                time.sleep(1)
              subprocess.check_call(('ssh', '-n', '-i', self.ssh_key,
                '-o', 'BatchMode=yes',
                '-o', 'UserKnownHostsFile=' + os.devnull,
                '-o', 'StrictHostKeyChecking=no',
                '-p', str(ssh[1]), 'root@' + ssh[0], init + command), env=env)
          finally:
            p.stop()
          break
      finally:
        shutil.rmtree(tmp)
    return [location]
