import re
import os

#fping = open('fping.txt')
#for ips in fping:
#    ips= fping.read()

#ips = ["s1", "s3", "s4", "s5", "s6"]
ips = ["172.20.201.4", "172.20.201.50", "172.20.201.52"]

sudo = 'sudo'


def nmap():
    for hosts in ips:
        print('--'*56)
        print(f'Device: {hosts}')
        # Save nmap output file 
        nmapFile = f'{sudo} nmap -sT -sV -O -Pn {hosts} > {hosts}.cfg'
        cmdFile = os.system(nmapFile)

        # Run nmap
        nmap = f'{sudo} nmap -sT -sV -O -Pn {hosts}'
        cmd = os.system(nmap)
        #print(cmd)
        
        f = open(f'{hosts}.cfg')
        cmdRead = f.read()
        #print(cmdRead)

        # Regex pattern to find contexts in device
        regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")
        regex_os = re.compile(r"Service Info: (?P<info_OS>\S.+)")
        regex_ports = re.compile(r"(?:ssh)")

        print('--'*56)
        print('Getting Informations')
        hostname = regex.search(str(cmdRead))
        match = hostname.group('hostname')
        print(f'Hostname: {match}')

        systemOS = regex_os.search(str(cmdRead))
        matchOS = systemOS.group('info_OS')
        print(f'System OS: {matchOS}')
nmap()