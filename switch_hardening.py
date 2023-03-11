from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import re
import net_conn
import auth

"""
The main proposal here is to identify all interfaces unused on environment and disable to avoid man-in-the-middle.
I'm using Netbox as Source of Truth to found and connect devices. 
The function "net_conn.py" was imported to use Netmiko and function "auth.py" to pass all the parameters to authenticate.
"""

nb_api = list(auth.nb.dcim.devices.filter("mgmt",model="9200"))

"""
Loop devices find on Netbox
"""
for ip in nb_api:
    ipadd = str(ip)
    ios = net_conn.netmiko_nxos(ipadd)
    print(f"Connecting to {ipadd}")
    
    """
    Handle device not reachable exceptions in Netmiko
    """
    try:
        net_connect = ConnectHandler(**ios)
        output = net_connect.send_command("show interface status | in notconnect")
    except (NetmikoTimeoutException):
        print(f'Timeout to device: {ipadd}')
        continue
    except (AuthenticationException):
        print(f'Authentication failure: {ipadd}')
        continue
    except (EOFError):
        print(f'End of file while attempting device {ipadd}')
        continue
    except (SSHException):
        print(f'SSH Issue. Are you sure SSH is enabled? {ipadd}')
        continue
    except Exception as unknown_error:
        print(f'Some other error: {str(unknown_error)}')
        continue

    """
    All environment has kinds of vendors, depends on devices the command should be different. In this case,
    it is important to check which device is connecting to send the appropriate command. So I start to check
    the version, if it is NX-OS send nxos command or if IOS send ios command.
    """

    # Types of devices
    list_versions = ['NX-OS','IOS']

    # Check software versions
    for software_ver in list_versions:
        print ('Checking for ' + software_ver)
        output_version = net_connect.send_command('show version')
        int_version = 0 # Reset integer value
        int_version = output_version.find(software_ver) # Check software version
        if int_version > 0:
            print ('Software version found: ' + software_ver)
            break
        else:
            print ('Did not find ' + software_ver)

    if software_ver == 'NX-OS':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_command('show interface status | in xcvrAbsen')
    elif software_ver == 'IOS':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_command('show interface status | in notconnect')
    
    """
    Regex pattern from NXOS
    """    
    int_pattern = re.compile(r"(?P<interface>\S+[A-Za-z][0-9].[0-9].[0-9]*)")
    
    """
    Handle exception when does not have a specific match 
    """
    try:
        match = int_pattern.search(output)
        interface = match.group("interface")
    except (AttributeError):
        print('No such attribute')
        continue
    
    # Regex pattern
    all_int = re.findall(int_pattern, output)

    """
    Loop to print all condition interfaces
    """
    for int in all_int:
        print(f'{int}')

        """
        Device Hardening - Disable all interfaces matched with "notconnect or xcvrAbsent"
        """
        cmd = net_connect.send_config_set(["interface " + int, "shutdown"])
        print(cmd)
