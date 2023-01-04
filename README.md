# cybersec

Looking for pattern as hostname, IP, ports, OS in nmap output.

## fping
Using fping to find ICMP requests on network
fping -a -g 192.168.0.0/24 2>/dev/null > fping.txt

## NMAP
run nmap in a file using -iL fping.txt to use only ICMP response.
e.g
nmap -sT -Sv -O -Pn -iL fping.txt

## search_nmap.py
Is a function that have a regex patterns to find a specfic information o nmap output file

# Regex pattern to find contexts in device
regex = re.compile(r"Nmap scan report for (?P<hostname>\w.+)")<\br>
regex_os = re.compile(r"Service Info: (?P<OS>\S.+)")
