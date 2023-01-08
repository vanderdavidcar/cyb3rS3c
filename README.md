# CyberSec

Looking for pattern as hostname, IP, vulnerable ports, OS in nmap output.

# The Most Vulnerable Ports to Check When Pentesting
vulnPorts = ["20/tcp", "21/tcp", "22/tcp","23/tcp","25/tcp","69/tcp","80/tcp","8080/tcp","8443/tcp","443/tcp","53/tcp","3389/tcp", "137/tcp","139/tcp", "145/tcp", "445/tcp"]

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
