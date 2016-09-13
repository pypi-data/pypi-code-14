import os
import subprocess

import osnap.const
import osnap.util


def add_package_mac(package, verbose):
    cmd = os.path.join(osnap.const.python_folder, 'bin', 'pip3') + ' install ' + package
    if verbose:
        print('executing %s' % str(cmd))
    return subprocess.call(cmd, shell=True, env={})


def create_python_mac(version, clean_cache, verbose):
    """
    Create a full, stand-alone python installation with the required packages
    """

    osnap.util.make_dir(osnap.const.python_folder, True, verbose)
    osnap.util.make_dir(osnap.const.CACHE_FOLDER, clean_cache, verbose)

    install_pyrun_script = 'install-pyrun.sh'
    osnap.util.get('https://downloads.egenix.com/python/install-pyrun', '.', install_pyrun_script, verbose)
    os.chmod(install_pyrun_script, 0o755)

    cmd = [install_pyrun_script]
    # version here is x.y (e.g. 3.5), not z.y.z (e.g. not 3.5.2)
    cmd.append('--python=%s' % version)
    # version 2.2.1 produces a "Segmentation fault: 11" error when python is run so use a prior version.
    cmd.append('--pyrun=2.2.0')

    # pip version explicit specification is a workaround since "--pip-version=latest" doesn't work
    # for install-pyrun.sh ( I get "sed: illegal option -- r" ).  Also, same for setuptools.
    # todo: either get the script fixed or dynamically determine the latest pip and setuptools
    cmd.append('--pip-version=8.1.2')
    cmd.append('--setuptools-version=26.0.0')

    cmd.append('-l')  # log

    cmd.append(osnap.const.python_folder)

    cmd = ' '.join(cmd)  # shell=True needs a string, not a list

    if verbose:
        print('cmd : %s' % str(cmd))
        print('env : %s' % str(osnap.const.ENV))
    subprocess.run(cmd, shell=True, env=osnap.const.ENV)






