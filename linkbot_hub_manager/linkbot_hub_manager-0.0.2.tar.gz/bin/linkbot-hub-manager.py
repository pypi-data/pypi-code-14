#!/usr/bin/env python3

import bottle
from passlib.hash import sha256_crypt as sha256
import re
import subprocess

DEFAULT_PASSWORD='$5$rounds=535000$QultdcXXlhMPqAXe$5a1iLNvR69uyuwAKaTQc5Dlwu/lWXDJO4/DT1/iRnt5'

def check(user, pw):
    if user != 'admin':
        return False
    # See if our password file exists
    try:
        with open('/boot/barobo_password', 'r') as pwfile:
            hash = pwfile.read().strip()
    except FileNotFoundError:
        hash = DEFAULT_PASSWORD
    return sha256.verify(pw, hash)

@bottle.route('/')
@bottle.auth_basic(check)
def main_page():
    try:
        dpkg_status = subprocess.check_output(['dpkg', '-s', 'linkbotd'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        dpkg_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    try:
        linkbotd_status = subprocess.check_output(['systemctl', 'status', 'linkbotd'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        linkbotd_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    linkbotd_status = """
        <h1> Status </h1>
        <form action="/system/reboot"> <input type="submit" value="Reboot" /> </form>
        <form action="/system/shutdown"> <input type="submit" value="Shut down" /> </form>
        <h2> linkbotd </h2>
        <form action="/linkbotd/start"> <input type="submit" value="Start" /> </form>
        <form action="/linkbotd/stop"> <input type="submit" value="Stop" /> </form>
        <form action="/linkbotd/restart"> <input type="submit" value="Restart" /> </form>
        Note: Upgrade may take several minutes to complete. Please click on the link only once.
        <form action="/linkbotd/upgrade"> <input type="submit" value="Upgrade" /> </form>
        <form action="/linkbotd/logs"> <input type="submit" value="Logs" /> </form>
        <h3> Package Info </h3>
        <pre>{}</pre>
        <h3> Daemon Status </h3>
        <pre>{}</pre>
    """.format(
        dpkg_status,
        linkbotd_status)

    try:
        prex_package = subprocess.check_output(['pip3', 'show', 'prex'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        prex_package= 'Error code {}: {}'.format(e.returncode, e.output.decode())

    try:
        prex_status = subprocess.check_output(['systemctl', 'status', 'prex'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        prex_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())
        
    prex_status = """
        <hr>
        <h2> prex </h2>
        <form action="/prex/start"> <input type="submit" value="Start" /> </form>
        <form action="/prex/stop"> <input type="submit" value="Stop" /> </form>
        <form action="/prex/restart"> <input type="submit" value="Restart" /> </form>
        Note: Upgrade may take several minutes to complete. Please click on the link only once.
        <form action="/prex/upgrade"> <input type="submit" value="Upgrade" /> </form>
        <form action="/prex/logs"> <input type="submit" value="Logs" /> </form>
        <h3> Package Info </h3>
        <pre>{}</pre>
        <h3> Daemon Status </h3>
        <pre>{}</pre>
    """.format(
        prex_package,
        prex_status )

    try:
        pylinkbot_status = subprocess.check_output(['pip3', 'show', 'pylinkbot3'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        pylinkbot_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    pylinkbot_status = """
        <hr>
        <h2> PyLinkbot3 </h2>
        Note: Upgrade may take several minutes to complete. Please click on the link only once.
        <form action="/pylinkbot3/upgrade"> <input type="submit" value="Upgrade" /> </form>
        <h3> Package Info </h3>
        <pre>{}</pre>
    """.format(pylinkbot_status)

    try:
        liblinkbot_status = subprocess.check_output(['dpkg', '-s', 'liblinkbot']).decode()
    except subprocess.CalledProcessError as e:
        liblinkbot_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    liblinkbot_status = """
        <hr>
        <h2> liblinkbot </h2>
        Note: Upgrade may take several minutes to complete. Please click on the link only once.
        <form action="/liblinkbot/upgrade"> <input type="submit" value="Upgrade" /> </form>
        <h3> Package Info </h3>
        <pre>{}</pre>
    """.format(liblinkbot_status)

    try:
        firmware_status = subprocess.check_output(['dpkg', '-s', 'linkbot-firmware']).decode()
    except subprocess.CalledProcessError as e:
        firmware_status = 'Error code {}: {}'.format(e.returncode, e.output.decode())

    firmware_status = """
        <hr>
        <h2> Linkbot Firmware </h2>
        Note: Upgrade may take several minutes to complete. Please click on the link only once.
        <form action="/linkbot-firmware/upgrade"> <input type="submit" value="Upgrade" /> </form>
        <h3> Package Info </h3>
        <pre>{}</pre>
    """.format(firmware_status)
    

    return linkbotd_status + prex_status + pylinkbot_status + liblinkbot_status + \
        firmware_status + """
        <h1> Change Password </h1>
        <form action="/change_password" method="post">
            New Password: <input name="password" type="password" />
            Repeat new password: <input name="repeat_password" type="password" />
            <input type="submit" value="Submit" />
        </form>
    """

@bottle.post('/change_password')
@bottle.auth_basic(check)
def change_password():
    password = bottle.request.forms.get('password')
    repeat_password = bottle.request.forms.get('repeat_password') 
    if password != repeat_password:
        return 'Error: Passwords do not match.'
    try:
        with open('/boot/barobo_password', 'w') as pwfile:
            hash = sha256.encrypt(password)
            pwfile.write(hash)
            return 'OK'
    except Exception as e:
        return 'Could not change password: {}'.format(e)

@bottle.route('/<module>/version')
def handle_version(module):
    if module in ['liblinkbot', 'linkbotd', 'linkbot-firmware']:
        return handle_dpkg_version(module)
    elif module in ['prex', 'pylinkbot3']:
        return handle_pip_version(module)
    else:
        return "Cannot get version of module: {}".format(module)

@bottle.route('/<module>/<function>')
@bottle.auth_basic(check)
def handle_all(module, function):
    if function == 'restart':
        if module in ['linkbotd', 'prex']:
            return handle_restart(module)
        else:
            return "Cannot restart module: {}".format(module)

    if function == 'stop':
        if module in ['linkbotd', 'prex']:
            return handle_stop(module)
        else:
            return "Cannot stop module: {}".format(module)

    if function == 'start':
        if module in ['linkbotd', 'prex']:
            return handle_start(module)
        else:
            return "Cannot start module: {}".format(module)

    if function == 'reboot':
        try:
            output = subprocess.check_output(['/sbin/reboot'])
            return 'OK'
        except Exception as e:
            return 'Could not restart {}: {}'.format(module, e)

    if function == 'shutdown':
        try:
            output = subprocess.check_output(['/sbin/shutdown', '-h', 'now'])
            return 'OK'
        except Exception as e:
            return 'Could not shutdown {}: {}'.format(module, e)

    if function == 'upgrade':
        return handle_upgrade(module)

    if function == 'logs':
        return handle_logs(module)

def handle_dpkg_version(module):
    try:
        output = subprocess.check_output(['dpkg', '-s', module], stderr=subprocess.STDOUT)
        m = re.search('Version: (.*)', output.decode())
        return m.group(1)
    except Exception as e:
        return "Could not get version on module '{}'".format(module) + str(e)
            
def handle_pip_version(module):
    try:
        output = subprocess.check_output(['pip3', 'show', module], stderr=subprocess.STDOUT)
        m = re.search('Version: (.*)', output.decode())
        return m.group(1)
    except:
        return "Could not get version on module '{}'".format(module)

def handle_restart(module):
    try:
        output = subprocess.check_output(['systemctl', 'restart', module], stderr=subprocess.STDOUT)
        return 'OK'
    except Exception as e:
        return 'Could not restart {}: {}'.format(module, e)

def handle_stop(module):
    try:
        output = subprocess.check_output(['systemctl', 'stop', module], stderr=subprocess.STDOUT)
        return 'OK'
    except Exception as e:
        return 'Could not stop {}: {}'.format(module, e)

def handle_start(module):
    try:
        output = subprocess.check_output(['systemctl', 'start', module], stderr=subprocess.STDOUT)
        return 'OK'
    except Exception as e:
        return 'Could not start {}: {}'.format(module, e)

def handle_upgrade(module):
    if module in ['linkbotd', 'liblinkbot', 'linkbot-firmware']:
        try:
            output = subprocess.check_output(['apt-get', 'update'])
            output += subprocess.check_output(['apt-get', 'install', '-y', module])
            return 'OK'
        except subprocess.CalledProcessError as e:
            return "Could not upgrade. Error code: {} : {}".format(e.returncode, e.output.decode())
    elif module in ['prex', 'pylinkbot3']:
        try:
            output = subprocess.check_output(['pip3', 'install', '--upgrade', module])
            return 'OK'
        except subprocess.CalledProcessError as e:
            return "Could not upgrade. Error code: {} : {}".format(e.returncode, e.output.decode())
    else:
        return 'Cannot upgrade module "{}".'.format(module)

def handle_logs(module):
    if module in ['prex', 'linkbotd']:
        try:
            output = subprocess.check_output(['journalctl', '-u', module], stderr=subprocess.STDOUT)
            return '<pre>'+output.decode()+'</pre>'
        except subprocess.CalledProcessError as e:
            return "Error {} obtaining logs: {}".format(e.returncode, e.output.decode())

    else:
        return "Cannot get logs for module '{}'.".format(module)
            

bottle.run(host='0.0.0.0', port=8080, debug=True)
