import re
import os

"""
List of IP Address that should be scanning, below two ways can you use with a simple list or open a file 
that have all IPs you need
"""
ips = ["s1", "s3", "s4", "s5", "s6"]

# Privilege mode
sudo = 'sudo'

# Regex pattern to find contexts in device
regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")
regex_os = re.compile(r"Service Info: (?P<info_OS>\S.+)")
open_ports = re.compile(r"(?P<open_ports>\d[0-9]*\w.tcp.+)")
open_tcp = re.compile(r"(?P<open_tcp>\d[0-9]*\w.tcp)")

def nmap():
    for hosts in ips:
        print('--'*56)
        print(f'Device: {hosts}\n')
        
        # Save nmap output file 
        nmapFile = f'{sudo} nmap -sT -sV -O -Pn {hosts} > {hosts}.cfg'
        cmdFile = os.system(nmapFile)

        # Run nmap
        nmap = f'{sudo} nmap -sT -sV -O -Pn'
        cmd = os.system(f'{nmap}{hosts}')
        
        f = open(f'{hosts}.cfg')
        cmdRead = f.read()
        
        # Collect information by regular expression pattern
        print('Getting Informations\n')
        hostname = regex.search(str(cmdRead))
        match = hostname.group('hostname')
        print(f'Hostname: {match}')

        systemOS = regex_os.search(str(cmdRead))
        matchOS = systemOS.group('info_OS')
        print(f'System OS: {matchOS}\n')

        # Different way to find specific information using regex pattern
        openOut = re.findall(open_ports,cmdRead)
        
        # Loop to find open ports
        for i in openOut:
            if "open" in i:
                print(f'Open Port:{i}')
        print(f'\n')

        # Open TCP ports on nmap scan
        openTCP = re.findall(open_tcp,cmdRead)
        
        # Vuln ports to find in NMAP
        vulnPorts = ["21/tcp", "23/tcp", "3389/tcp", "139/tcp", "145/tcp"]

        # Find users that doesn't match with variable users
        for ports in openTCP:
            if ports in vulnPorts:
                print(f'Vulnerable Port:{ports}')

        arquivo = open('output.txt', 'w')
        print('informação', file=arquivo) 
        arquivo.close()
nmap()