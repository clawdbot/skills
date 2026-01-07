#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "rich"]
# ///
"""Digital Ocean CLI - Manage droplets, domains, and infrastructure.

Usage:
    do.py account               Show account info
    do.py droplets              List all droplets
    do.py droplet <id>          Get droplet details
    do.py domains               List domains
    do.py records <domain>      List DNS records for domain
    do.py power-on <id>         Power on droplet
    do.py power-off <id>        Power off droplet
    do.py reboot <id>           Reboot droplet
"""

import json
import os
import sys
import httpx
from rich.console import Console
from rich.table import Table

console = Console()

API_URL = "https://api.digitalocean.com/v2"
TOKEN = os.environ.get("DO_API_TOKEN")


def api_get(endpoint: str, params: dict = None) -> dict:
    if not TOKEN:
        console.print("[red]Error: DO_API_TOKEN not set[/red]")
        sys.exit(1)
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    resp = httpx.get(f"{API_URL}{endpoint}", params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def api_post(endpoint: str, data: dict = None) -> dict:
    if not TOKEN:
        console.print("[red]Error: DO_API_TOKEN not set[/red]")
        sys.exit(1)
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    resp = httpx.post(f"{API_URL}{endpoint}", json=data, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def cmd_account():
    """Show account info."""
    data = api_get("/account")
    acct = data.get("account", {})
    console.print(f"[bold]Email:[/bold] {acct.get('email')}")
    console.print(f"[bold]Status:[/bold] {acct.get('status')}")
    console.print(f"[bold]Droplet Limit:[/bold] {acct.get('droplet_limit')}")
    console.print(f"[bold]Email Verified:[/bold] {acct.get('email_verified')}")


def cmd_droplets():
    """List all droplets."""
    data = api_get("/droplets")
    droplets = data.get("droplets", [])
    
    if not droplets:
        console.print("[dim]No droplets found[/dim]")
        return
    
    table = Table(title="Droplets")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status")
    table.add_column("IP")
    table.add_column("Region")
    table.add_column("Size")
    
    for d in droplets:
        ip = ""
        for net in d.get("networks", {}).get("v4", []):
            if net.get("type") == "public":
                ip = net.get("ip_address", "")
                break
        
        status_style = "green" if d.get("status") == "active" else "yellow"
        table.add_row(
            str(d.get("id")),
            d.get("name"),
            f"[{status_style}]{d.get('status')}[/{status_style}]",
            ip,
            d.get("region", {}).get("slug", ""),
            d.get("size_slug", "")
        )
    
    console.print(table)


def cmd_droplet(droplet_id: str):
    """Get droplet details."""
    data = api_get(f"/droplets/{droplet_id}")
    d = data.get("droplet", {})
    
    ip = ""
    for net in d.get("networks", {}).get("v4", []):
        if net.get("type") == "public":
            ip = net.get("ip_address", "")
            break
    
    console.print(f"[bold cyan]ID:[/bold cyan] {d.get('id')}")
    console.print(f"[bold]Name:[/bold] {d.get('name')}")
    console.print(f"[bold]Status:[/bold] {d.get('status')}")
    console.print(f"[bold]IP:[/bold] {ip}")
    console.print(f"[bold]Region:[/bold] {d.get('region', {}).get('name')}")
    console.print(f"[bold]Size:[/bold] {d.get('size_slug')} ({d.get('memory')}MB RAM, {d.get('vcpus')} vCPUs)")
    console.print(f"[bold]Disk:[/bold] {d.get('disk')}GB")
    console.print(f"[bold]Image:[/bold] {d.get('image', {}).get('name')}")
    console.print(f"[bold]Created:[/bold] {d.get('created_at')}")
    
    # Tags
    tags = d.get("tags", [])
    if tags:
        console.print(f"[bold]Tags:[/bold] {', '.join(tags)}")


def cmd_domains():
    """List domains."""
    data = api_get("/domains")
    domains = data.get("domains", [])
    
    if not domains:
        console.print("[dim]No domains found[/dim]")
        return
    
    table = Table(title="Domains")
    table.add_column("Name", style="cyan")
    table.add_column("TTL")
    
    for d in domains:
        table.add_row(d.get("name"), str(d.get("ttl", "")))
    
    console.print(table)


def cmd_records(domain: str):
    """List DNS records for domain."""
    data = api_get(f"/domains/{domain}/records")
    records = data.get("domain_records", [])
    
    if not records:
        console.print(f"[dim]No records found for {domain}[/dim]")
        return
    
    table = Table(title=f"DNS Records: {domain}")
    table.add_column("ID", style="dim")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Data")
    table.add_column("TTL")
    
    for r in records:
        table.add_row(
            str(r.get("id")),
            r.get("type"),
            r.get("name"),
            r.get("data", "")[:50],
            str(r.get("ttl", ""))
        )
    
    console.print(table)


def cmd_action(droplet_id: str, action: str):
    """Perform action on droplet."""
    data = api_post(f"/droplets/{droplet_id}/actions", {"type": action})
    act = data.get("action", {})
    console.print(f"[green]✓[/green] Action '{action}' initiated (ID: {act.get('id')}, Status: {act.get('status')})")


def main():
    if len(sys.argv) < 2:
        console.print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "account":
        cmd_account()
    elif cmd == "droplets":
        cmd_droplets()
    elif cmd == "droplet" and len(sys.argv) > 2:
        cmd_droplet(sys.argv[2])
    elif cmd == "domains":
        cmd_domains()
    elif cmd == "records" and len(sys.argv) > 2:
        cmd_records(sys.argv[2])
    elif cmd == "power-on" and len(sys.argv) > 2:
        cmd_action(sys.argv[2], "power_on")
    elif cmd == "power-off" and len(sys.argv) > 2:
        cmd_action(sys.argv[2], "power_off")
    elif cmd == "reboot" and len(sys.argv) > 2:
        cmd_action(sys.argv[2], "reboot")
    else:
        console.print(__doc__)


if __name__ == "__main__":
    main()
