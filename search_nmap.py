import re

f = open('nmap_output.txt', 'r')
for nmap_output in f:
    nmap_output= f.read()

# Regex pattern to find contexts in device
regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")
regex_os = re.compile(r"Service Info: (?P<OS>\S.+)")
regex_ports = re.compile(r"(?:ssh)")
   
def nmap():
    hosts = re.findall(regex,nmap_output)
    os_system = re.findall(regex_os, nmap_output)
    
    for i in hosts:
        if i:
            print(f'Host: {i} System:{os_system}')
    
    #ports = re.findall(regex_ports, nmap_output)
#
    #for n in hosts:
    #    print(f'Host: {n}')
    #    
    #for i in os_system:
    #    if "linux" in i:
    #        print(f'Host: {n} System: {i}')
    #
    #for p in ports:
    #    print(p)
nmap()