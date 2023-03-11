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
nb_api_ios = list(auth.nb.dcim.devices.filter("mgmt",model="9200"))

"""
Loop devices found on Netbox database
"""
for ip in nb_api_ios:
    ipadd = str(ip)
    ios = net_conn.netmiko_ios(ipadd)
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
    Regex pattern to find all kinds of interfaces as Gigabit, Ethernet, TenGigabit and so on.
    """    
    int_pattern = re.compile(r"(?P<interface>\S+[A-Za-z][0-9].[0-9].[0-9]*)")
    
    """
    Handle exception when does not have a specific match in line 30 in this case "notconnect"
    """
    try:
        match = int_pattern.search(output)
        interface = match.group("interface")
    except (AttributeError):
        print('No such attribute "notconnect interfaces"')
        continue
    
    # Regex pattern
    all_int = re.findall(int_pattern, output)

    """
    Loop to print all interfaces matched in that condition
    """
    for int in all_int:
        print(f'{int}')

        """
        Device Hardening - Disable all interfaces that match after founded
        """
        cmd = net_connect.send_config_set(["interface " + int, "shutdown"])
        print(cmd)
