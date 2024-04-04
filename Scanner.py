from scapy.all import *
import random
import string
import time

# Dictionary to store scan results
scan_results = {}

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def spoofed_dns_request(target_ip, spoofed_ip):
    random_subdomain = generate_random_string(6)
    resolver_ip_hex = hex(int(ipaddress.IPv4Address(target_ip)))[2:]  # Convert resolver IP to hex
    scan_identifier = "02ae52c7"  # Example scan identifier
    dns_query = random_subdomain + "." + resolver_ip_hex + ".s1.drakkardns.com"
    dns_packet = IP(src=spoofed_ip, dst=target_ip) / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname=dns_query))
    response = sr1(dns_packet, verbose=False, timeout=1)
    if response:
        scan_results[target_ip] = {"spoofed_request": True, "spoofed_response": response.summary()}
    else:
        scan_results[target_ip] = {"spoofed_request": True, "spoofed_response": "No response"}

def non_spoofed_dns_request(target_ip):
    random_subdomain = generate_random_string(6)
    resolver_ip_hex = "02ae52c7"  # Example resolver IP hex
    scan_identifier = "n1"  # Non-spoofed identifier
    dns_query = random_subdomain + "." + resolver_ip_hex + "." + scan_identifier + ".drakkardns.com"
    dns_packet = IP(dst=target_ip) / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname=dns_query))
    response = sr1(dns_packet, verbose=False, timeout=1)
    if response:
        scan_results[target_ip]["non_spoofed_response"] = response.summary()
    else:
        scan_results[target_ip]["non_spoofed_response"] = "No response"

def scan_network(network):
    for i in range(1, 255):
        target_ip = network + "." + str(i)
        scan_results[target_ip] = {}
        spoofed_dns_request(target_ip, network)
        time.sleep(0.1)  # Adjust as necessary to avoid overwhelming the network
        non_spoofed_dns_request(target_ip)
        time.sleep(0.1)

def save_results_to_file():
    with open("scan_results.txt", "w") as f:
        for target_ip, result in scan_results.items():
            f.write(f"Target IP: {target_ip}\n")
            f.write(f"Spoofed request sent: {result.get('spoofed_request')}\n")
            f.write(f"Spoofed response: {result.get('spoofed_response')}\n")
            f.write(f"Non-spoofed response: {result.get('non_spoofed_response')}\n")
            f.write("\n")

if __name__ == "__main__":
    network_to_scan = "1.2.3"  # Example network to scan
    scan_network(network_to_scan)
    save_results_to_file()