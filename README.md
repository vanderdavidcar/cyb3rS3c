# CyberSec

Looking for pattern as hostname, IP, ports, OS in nmap output.

## fping
Using fping to find ICMP requests on network</br>
e.g</br>
fping -a -g 192.168.0.0/24 2>/dev/null > fping.txt

## NMAP
run nmap in a file using -iL fping.txt to use only ICMP response.</br>
e.g</br>
nmap -n - sS --max-os-tries 1 -sT -Sv -O -Pn -v -iL fping.txt

## search_nmap.py
Is a function that has a regex patterns to find a specfic information o nmap output file.

## Regex pattern examples
regex = re.compile(r"Nmap scan report for (\w.+)")</br>
regex_os = re.compile(r"Service Info: (\S.+)")
