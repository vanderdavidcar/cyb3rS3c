import re
import os

ips = ["s1", "s3", "s4", "s5", "s6"]
sudo = 'sudo'

# Regex pattern to find contexts in device
regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")
regex_os = re.compile(r"Service Info: (?P<info_OS>\S.+)")
open_ports = re.compile(r"(?P<open_ports>\d[0-9]*\w.tcp.+)")

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
                print(f'Open Port: {i}')
        
        """
        Looping below does not work yet, I'm working in this logic to find only a vulnerable ports based on list "vuln"
        """
#        # Looking for exploitable ports open on device
#        vulnPorts = [21, 23, 135, 139, 445, 3389]
#        n = open(str(vulnPorts))
#        #expVuln = n.read()
#        print(n)
#        
#        # Looping to find vulnerableports
#        for ports in openOut:
#            if vulnPorts in ports:
#                print(f'Vulnerable Port: {ports}')
#            else:
#                print(f'There are no Vulnerable port in {hosts}')
nmap()