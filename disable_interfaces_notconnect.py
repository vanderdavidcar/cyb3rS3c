from netmiko import ConnectHandler
from dotenv import load_dotenv
import re
import net_conn

load_dotenv()


lab = ["brbsa-bt02-mgmt-stk1-1"]

# Informações de conexão com o switch
for ip in lab:
    ios = net_conn.netmiko_ios(ip)
    print(f"Connecting to {str(ip)}")

    net_connect = ConnectHandler(**ios)
    output = net_connect.send_command("show interfaces | in notconnect")

    # List of regex pattern from NXOS
    int_pattern = re.compile(r"(?P<interface>\S+[A-Za-z][0-9].[0-9].[0-9]*)")

    match = int_pattern.search(output)
    interface = match.group("interface")

    # Regex pattern to users and priv_lvl
    all_int = re.findall(int_pattern, output)

    for int in all_int:
        # print(f'interface {int}')
        cmd = net_connect.send_config_set(["interface " + int, "shutdown"])
        print(cmd)
