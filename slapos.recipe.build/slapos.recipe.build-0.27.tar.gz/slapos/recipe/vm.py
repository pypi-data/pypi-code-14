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

is_true = ('false', 'true').index

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
    # Workaround for spurious "No network interfaces detected"
    # See https://bugs.debian.org/842201
    fb = false

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
    passwd/root-login = true
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
      if preseed and preseed[0] != '#':
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

    vm_run = is_true(options.get('vm.run', 'true'))
    packages = ['ssh', 'sudo'] if vm_run else []
    packages += options.get('packages', '').split()
    if packages:
      cmdline['pkgsel/include'] = ','.join(packages)

    generated = []
    for x, p in (('root', 'passwd/root-login'),
                 ('user', 'passwd/make-user')):
      if is_true(cmdline[p]):
        p = 'passwd/%s-password' % x
        if x == 'user':
          x = cmdline.get('passwd/username')
          if not x:
            raise UserError('passwd/username is empty')
          cmdline.setdefault('passwd/user-fullname', '')
        if not (cmdline.get(p) or cmdline.get(p + '-crypted')):
          cmdline[p] = cmdline[p + '-again'] = passwd = generatePassword()
          generated.append((x, passwd))

    env = self.environ

    location = self.vm
    with building_directory(location):
      if vm_run:
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
        open_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
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

      if generated:
        fd = os.open(join(location, 'passwd'), open_flags, 0600)
        try:
          for generated in generated:
            os.write(fd, "%s:%s\n" % generated)
        finally:
          os.close(fd)

    return [location]


class RunRecipe(BaseRecipe):

  init = """set -e
cd /mnt; set %s; mkdir -p $*; for tag; do
  mount -t 9p -o trans=virtio,version=9p2000.L,noatime $tag $tag
done
"""

  command = """set -e
reboot() {
  unset -f reboot
  %s%s
  (while pgrep -x sshd; do sleep 1; done >/dev/null; %sreboot
  ) >/dev/null 2>&1 &
  exit
}
map() {
  local x=${1#%s}; case $x in $1) exit 1;; ''|/*) ;; *) exit 1;; esac
  echo /mnt/buildout$x
}
PARTDIR=`map %s`
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
    init = self.init % ' '.join(self.mount_dict)
    user = options.get('user')
    if user == 'root':
      init += 'cd; exec sh'
      sudo = ''
    else:
      sudo = 'sudo '
      if not user:
        init += """user=slapos gid=%s
cd /etc/sudoers.d
[ -f $user ] || {
  groupadd -g $gid $user || :
  useradd -m -u %s -g $gid $user
  echo $user ALL=NOPASSWD: ALL >$user
  chmod 440 $user
}
""" % (os.getgid(), os.getuid())
        user = '$user'
      init += 'exec su -ls /bin/sh ' + user

    header = self.command % (
      sudo, options.get('stop-ssh', 'systemctl stop ssh'), sudo,
      self.buildout['buildout']['directory'], location)
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
          qemu = Popen(args, stderr=subprocess.PIPE, env=dict(env,
            TMPDIR=location, # for snapshot
            ))
          try:
            while not select.select((qemu.stderr,), (), (), 1)[0]:
              if os.path.exists(vnc):
                break
            else:
              err = qemu.communicate()[1]
              sys.stderr.write(err)
              if ('could not set up host forwarding rule' in err and
                  hostfwd_retries):
                hostfwd_retries -= 1
                continue
              raise subprocess.CalledProcessError(qemu.returncode, args)
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
              args = ('ssh', '-i', self.ssh_key,
                '-o', 'BatchMode=yes',
                '-o', 'UserKnownHostsFile=' + os.devnull,
                '-o', 'StrictHostKeyChecking=no',
                '-p', str(ssh[1]), 'root@' + ssh[0], init)
              p = Popen(args, stdin=subprocess.PIPE, env=env)
              try:
                p.communicate(header + command)
                if p.returncode:
                  raise subprocess.CalledProcessError(p.returncode, args)
              finally:
                p.stop()
          finally:
            qemu.stop()
          break
      finally:
        shutil.rmtree(tmp)
    return [location]
