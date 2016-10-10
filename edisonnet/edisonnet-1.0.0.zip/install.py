import subprocess

HOME = "/opt/net"

def setup():
    print "Start Setup \n\n"

    # Step 1 - Copy source code to /home/root
    #subprocess.call("unzip -o edision.zip", shell=True)
    #subprocess.call("tar -xvf Pynetinfo-0.1.9.tar.gz", shell=True)

    # Step 2 - Intall Pynetinfo package
    #subprocess.call("cd Pynetinfo-0.1.9 && python setup.py install", shell=True)

    # Step 3 - Enable auto run service
    subprocess.call("mkdir -p " + HOME, shell=True)
    subprocess.call("cp edisonnet/* " + HOME, shell=True)
    subprocess.call("cp edisonnet/wpa_cli-actions.sh /etc/wpa_supplicant/wpa_cli-actions.sh", shell=True)
    subprocess.call("chmod 755 /etc/wpa_supplicant/wpa_cli-actions.sh", shell=True)
    subprocess.call("cp edisonnet/network_remote_config.service /lib/systemd/system/network_remote_config.service", shell=True)
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call("systemctl enable network_remote_config.service", shell=True)
    subprocess.call("systemctl start network_remote_config.service", shell=True)

    # Step 4 - Clean 
    #subprocess.call("rm -rf edision Pynetinfo-0.1.9 build", shell=True)

    print "\n\nSetup complete"

setup()
    
