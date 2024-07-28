import subprocess
import socket
from scapy.all import ARP, Ether, srp

COM = "com10"
PORT = "14550"
BAUDRATE = "115200"

SWITCH_IP = "192.168.1/24"
SHOULD_USE_NETWORK = True


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def get_ip_range(local_ip):
    ip_parts = local_ip.split('.')
    base_ip = '.'.join(ip_parts[:3]) + '.'
    return base_ip + '1/24'


def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=2, verbose=0)[0]

    ip_addresses = [(received.psrc, received.hwsrc) for sent, received in result]

    return ip_addresses


def get_ip_addresses_network():
    local_ip = get_local_ip()
    ip_range = get_ip_range(local_ip)
    ip_addresses = scan_network(ip_range)

    ip_list = []

    for ip, mac in ip_addresses:
        try:
            device_name = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            device_name = 'Unknown'
        print(f'IP: {ip}, Device: {device_name}')
        ip_list.append(ip)

    return ip_list


def get_ip_addresses_switch():
    return ["hard code ips here"]


def add_mavproxy_output(ip_list):
    command = f"mavproxy.exe --master={COM} " + " ".join([f"--out=udp:{ip}:{PORT}" for ip in ip_list]) + f" --out=udp:127.0.0.1:{PORT} --baudrate={BAUDRATE}"

    subprocess.run(command, shell=True, check=True)


# Retrieve IP addresses
ip_addresses = get_ip_addresses_network() if SHOULD_USE_NETWORK else get_ip_addresses_switch()
# Add MAVProxy output for each IP address
add_mavproxy_output(ip_addresses)