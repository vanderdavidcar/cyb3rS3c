import re
import os

"""
List of IP Address that should be scanning, below two ways can you use with a simple list or open a file 
that have all IPs you need
"""
ips = ["s1", "s3", "s4", "s5", "s6"]

"""
Another way to use a list of IPs
"""
IpAddres = open('nmap_output.txt', 'r')
for nmap_output in ips:
    nmap_output= ips.read()


# Privilege mode
sudo = 'sudo'

# List of vuln ports to find in NMAP scan
vulnPorts = ["21/tcp", "23/tcp", "3389/tcp", "139/tcp", "145/tcp", "445/tcp"]

"""
Regex pattern to use in function nmap()
"""

# Hostname
regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")

# Operation System (Windows, Linux, Unix, Cisco...)
regex_os = re.compile(r"Service Info: (?P<info_OS>\S.+)")

# Open Ports
open_ports = re.compile(r"(?P<open_ports>\d[0-9]*\w.tcp.+)")

# Variable used to find vulnerable ports
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

        # If vulnPort match with openTCP show us
        for ports in openTCP:
            if ports in vulnPorts:
                print(f'Vulnerable Port:{ports}')
nmap()