#!/usr/bin/env python3
"""
Network Scanner - Discover and identify devices on a network.
Outputs JSON or markdown with device information.

Usage:
    scan.py [network] [--dns DNS] [--json] [--config FILE]
    
Networks can be:
    - CIDR notation: 192.168.1.0/24
    - Named network from config file
    - "auto" to detect current network
"""

import subprocess
import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# Default config location
DEFAULT_CONFIG = Path.home() / ".config" / "network-scanner" / "networks.json"

# MAC vendor prefixes (common ones - extend as needed)
MAC_VENDORS = {
    "00:17:88": "Philips Hue",
    "b8:27:eb": "Raspberry Pi",
    "dc:a6:32": "Raspberry Pi",
    "e4:5f:01": "Raspberry Pi",
    "d8:3a:dd": "Raspberry Pi",
    "94:9f:3e": "Sonos",
    "b8:e9:37": "Sonos",
    "78:28:ca": "Sonos",
    "00:0c:29": "VMware",
    "00:50:56": "VMware",
    "00:1e:e0": "Urmet",
    "70:ee:50": "Netatmo",
    "ac:89:95": "AzureWave",
    "f0:99:bf": "Apple",
    "3c:22:fb": "Apple",
    "a4:83:e7": "Apple",
    "64:a2:00": "Apple",
    "a4:5e:60": "Apple",
    "14:98:77": "Apple",
    "00:1a:2b": "Ayecom (ASUS)",
    "fc:ec:da": "Ubiquiti",
    "78:8a:20": "Ubiquiti",
    "74:ac:b9": "Ubiquiti",
    "24:5a:4c": "Ubiquiti",
    "80:2a:a8": "Ubiquiti",
    "44:d9:e7": "Ubiquiti",
    "68:72:51": "Ubiquiti",
    "18:e8:29": "Ubiquiti",
    "9c:05:d6": "Synology",
    "00:11:32": "Synology",
}


def run_cmd(cmd, timeout=60):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except Exception as e:
        print(f"Command error: {e}", file=sys.stderr)
        return ""


def get_mac_vendor(mac):
    """Lookup MAC vendor from prefix."""
    if not mac:
        return None
    prefix = mac.lower()[:8]
    return MAC_VENDORS.get(prefix)


def reverse_dns(ip, dns_server=None):
    """Reverse DNS lookup."""
    cmd = f"dig +short -x {ip}"
    if dns_server:
        cmd += f" @{dns_server}"
    result = run_cmd(cmd, timeout=5)
    if result and "timed out" not in result.lower() and "connection refused" not in result.lower():
        return result.rstrip('.').split('\n')[0]
    return None


def detect_current_network():
    """Auto-detect current network CIDR."""
    # Get default route interface
    route = run_cmd("ip route | grep default | awk '{print $5}' | head -1")
    if not route:
        return None
    
    # Get IP and netmask for that interface
    ip_info = run_cmd(f"ip -o -4 addr show {route} | awk '{{print $4}}'")
    if ip_info:
        return ip_info
    return None


def load_config(config_path):
    """Load network configuration from JSON file."""
    if not config_path.exists():
        return {}
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Config error: {e}", file=sys.stderr)
        return {}


def save_example_config(config_path):
    """Save example configuration file."""
    example = {
        "networks": {
            "home": {
                "cidr": "192.168.1.0/24",
                "dns": "192.168.1.1",
                "description": "Home Network"
            },
            "office": {
                "cidr": "10.0.0.0/24",
                "dns": "10.0.0.1",
                "description": "Office Network"
            }
        }
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(example, f, indent=2)
    print(f"Example config saved to {config_path}", file=sys.stderr)


def scan_network(cidr, dns_server=None, use_sudo=True):
    """Scan network using nmap and gather device info."""
    devices = []
    
    # Run nmap scan - use sudo for MAC discovery
    print(f"Scanning {cidr}...", file=sys.stderr)
    sudo = "sudo " if use_sudo else ""
    nmap_cmd = f"{sudo}nmap -sn -oX - {cidr} 2>/dev/null"
    nmap_output = run_cmd(nmap_cmd, timeout=180)
    
    if not nmap_output:
        print("No nmap output - check permissions or network", file=sys.stderr)
        return devices
    
    # Parse nmap XML output
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(nmap_output)
    except Exception as e:
        print(f"Failed to parse nmap output: {e}", file=sys.stderr)
        return devices
    
    for host in root.findall('.//host'):
        status = host.find('status')
        if status is None or status.get('state') != 'up':
            continue
        
        device = {
            "ip": None,
            "hostname": None,
            "mac": None,
            "vendor": None,
        }
        
        # Get IP and MAC
        for addr in host.findall('address'):
            if addr.get('addrtype') == 'ipv4':
                device['ip'] = addr.get('addr')
            elif addr.get('addrtype') == 'mac':
                device['mac'] = addr.get('addr')
                device['vendor'] = addr.get('vendor') or get_mac_vendor(addr.get('addr'))
        
        # Get hostname from nmap
        hostnames = host.find('hostnames')
        if hostnames is not None:
            for hostname in hostnames.findall('hostname'):
                if hostname.get('type') == 'PTR' or not device['hostname']:
                    device['hostname'] = hostname.get('name')
        
        # Try reverse DNS if no hostname
        if not device['hostname'] and device['ip'] and dns_server:
            device['hostname'] = reverse_dns(device['ip'], dns_server)
        
        if device['ip']:
            devices.append(device)
    
    # Sort by IP
    devices.sort(key=lambda x: [int(p) for p in x['ip'].split('.')])
    
    return devices


def format_markdown(devices, network_name):
    """Format devices as markdown table."""
    lines = [
        f"### {network_name}",
        f"*Last scan: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "| IP | Name | MAC | Vendor |",
        "|----|------|-----|--------|"
    ]
    
    for d in devices:
        name = d['hostname'] or "—"
        mac = d['mac'] or "—"
        vendor = d['vendor'] or "—"
        lines.append(f"| {d['ip']} | {name} | {mac} | {vendor} |")
    
    lines.append("")
    lines.append(f"*{len(devices)} devices found*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Network Scanner - Discover devices on your network",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                        # Scan auto-detected network
    %(prog)s 192.168.1.0/24         # Scan specific CIDR
    %(prog)s home                   # Scan named network from config
    %(prog)s home --json            # Output as JSON
    %(prog)s --init-config          # Create example config file
    %(prog)s --list                 # List configured networks
"""
    )
    parser.add_argument("network", nargs="?", default="auto",
                        help="Network CIDR, name from config, or 'auto' (default)")
    parser.add_argument("--dns", help="DNS server for reverse lookups")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--no-sudo", action="store_true", 
                        help="Don't use sudo (may miss MAC addresses)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help=f"Config file path (default: {DEFAULT_CONFIG})")
    parser.add_argument("--init-config", action="store_true",
                        help="Create example config file")
    parser.add_argument("--list", action="store_true",
                        help="List configured networks")
    
    args = parser.parse_args()
    
    # Init config
    if args.init_config:
        save_example_config(args.config)
        return
    
    # Load config
    config = load_config(args.config)
    networks = config.get("networks", {})
    
    # List networks
    if args.list:
        if not networks:
            print("No networks configured. Run with --init-config to create example.")
        else:
            print("Configured networks:")
            for name, info in networks.items():
                print(f"  {name}: {info.get('cidr')} - {info.get('description', '')}")
        return
    
    # Determine network to scan
    if args.network == "auto":
        cidr = detect_current_network()
        if not cidr:
            print("Could not auto-detect network. Specify CIDR or network name.", file=sys.stderr)
            sys.exit(1)
        dns = args.dns
        name = f"Auto-detected ({cidr})"
    elif args.network in networks:
        net = networks[args.network]
        cidr = net['cidr']
        dns = args.dns or net.get('dns')
        name = net.get('description', args.network)
    elif '/' in args.network or args.network.replace('.', '').isdigit():
        # Looks like CIDR
        cidr = args.network
        dns = args.dns
        name = cidr
    else:
        print(f"Unknown network '{args.network}'. Use CIDR or configure in {args.config}", file=sys.stderr)
        sys.exit(1)
    
    # Scan
    devices = scan_network(cidr, dns, use_sudo=not args.no_sudo)
    
    # Output
    if args.json:
        output = {
            "network": name,
            "cidr": cidr,
            "devices": devices,
            "scanned_at": datetime.now().isoformat(),
            "device_count": len(devices)
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_markdown(devices, name))


if __name__ == "__main__":
    main()
