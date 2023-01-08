# CyberSec

Looking for pattern as hostname, IP, vulnerable ports, OS in nmap output.

## The Most Vulnerable Ports to Check When Pentesting
20, 21, 22, 23, 25, 69, 80, 8080, 8443, 443, 53, 3389, 137, 139, 145, 445</br>

## fping
Using fping to find ICMP requests on network</br>
e.g</br>
fping -a -g 192.168.0.0/24 2>/dev/null > fping.txt

## NMAP
There are many ways to run nmap

Using the simple way</br>
sudo nmap -sT -Sv -O -Pn -v -iL 192.168.0.21

run nmap specifying a file using -iL fping.txt to use only ICMP response.</br>
e.g</br>
sudo nmap -sT -Sv -O -Pn -v -iL fping.txt

## search_nmap.py
Is a function that has a regex patterns to find a specfic information o nmap output file.

## Regex pattern examples
regex = re.compile(r"Nmap scan report for (\w.+)")</br>
regex_os = re.compile(r"Service Info: (\S.+)")
