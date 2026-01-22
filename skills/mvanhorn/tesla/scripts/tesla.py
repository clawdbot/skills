#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "teslapy>=2.0.0",
# ]
# ///
"""
Tesla vehicle control via unofficial API.
"""

import argparse
import json
import os
import sys
from pathlib import Path

CACHE_FILE = Path.home() / ".tesla_cache.json"


def get_tesla(email: str):
    """Get authenticated Tesla instance."""
    import teslapy
    
    def custom_auth(url):
        print(f"\n🔐 Open this URL in your browser:\n{url}\n")
        print("Log in to Tesla, then paste the final URL here")
        print("(it will start with https://auth.tesla.com/void/callback?...)")
        return input("\nCallback URL: ").strip()
    
    tesla = teslapy.Tesla(email, authenticator=custom_auth, cache_file=str(CACHE_FILE))
    
    if not tesla.authorized:
        tesla.fetch_token()
        print("✅ Authenticated successfully!")
    
    return tesla


def get_vehicle(tesla):
    """Get first vehicle."""
    vehicles = tesla.vehicle_list()
    if not vehicles:
        print("❌ No vehicles found on this account", file=sys.stderr)
        sys.exit(1)
    return vehicles[0]


def cmd_auth(args):
    """Authenticate with Tesla."""
    email = args.email or os.environ.get("TESLA_EMAIL")
    if not email:
        email = input("Tesla email: ").strip()
    
    tesla = get_tesla(email)
    vehicle = get_vehicle(tesla)
    print(f"\n🚗 Found: {vehicle['display_name']} ({vehicle['vin']})")
    print(f"✅ Authentication cached at {CACHE_FILE}")


def cmd_status(args):
    """Get vehicle status."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    
    # Wake if needed
    if vehicle['state'] != 'online':
        print("⏳ Waking vehicle...", file=sys.stderr)
        vehicle.sync_wake_up()
    
    data = vehicle.get_vehicle_data()
    
    charge = data['charge_state']
    climate = data['climate_state']
    drive = data['drive_state']
    vehicle_state = data['vehicle_state']
    
    print(f"🚗 {vehicle['display_name']}")
    print(f"   State: {vehicle['state']}")
    print(f"   Battery: {charge['battery_level']}% ({charge['battery_range']:.0f} mi)")
    print(f"   Charging: {charge['charging_state']}")
    print(f"   Inside temp: {climate['inside_temp']}°C ({climate['inside_temp'] * 9/5 + 32:.0f}°F)")
    print(f"   Outside temp: {climate['outside_temp']}°C ({climate['outside_temp'] * 9/5 + 32:.0f}°F)")
    print(f"   Climate on: {climate['is_climate_on']}")
    print(f"   Locked: {vehicle_state['locked']}")
    print(f"   Odometer: {vehicle_state['odometer']:.0f} mi")
    
    if args.json:
        print(json.dumps(data, indent=2))


def cmd_lock(args):
    """Lock the vehicle."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    vehicle.command('LOCK')
    print("🔒 Vehicle locked")


def cmd_unlock(args):
    """Unlock the vehicle."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    vehicle.command('UNLOCK')
    print("🔓 Vehicle unlocked")


def cmd_climate(args):
    """Control climate."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    
    if args.action == 'on':
        vehicle.command('CLIMATE_ON')
        print("❄️ Climate turned on")
    elif args.action == 'off':
        vehicle.command('CLIMATE_OFF')
        print("🌡️ Climate turned off")
    elif args.action == 'temp':
        temp_c = (float(args.value) - 32) * 5/9 if args.fahrenheit else float(args.value)
        vehicle.command('CHANGE_CLIMATE_TEMPERATURE_SETTING', driver_temp=temp_c, passenger_temp=temp_c)
        print(f"🌡️ Temperature set to {args.value}°{'F' if args.fahrenheit else 'C'}")


def cmd_charge(args):
    """Control charging."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    
    if args.action == 'status':
        data = vehicle.get_vehicle_data()
        charge = data['charge_state']
        print(f"🔋 Battery: {charge['battery_level']}%")
        print(f"   Range: {charge['battery_range']:.0f} mi")
        print(f"   State: {charge['charging_state']}")
        print(f"   Limit: {charge['charge_limit_soc']}%")
        if charge['charging_state'] == 'Charging':
            print(f"   Time left: {charge['time_to_full_charge']:.1f} hrs")
            print(f"   Rate: {charge['charge_rate']} mph")
    elif args.action == 'start':
        vehicle.command('START_CHARGE')
        print("⚡ Charging started")
    elif args.action == 'stop':
        vehicle.command('STOP_CHARGE')
        print("🛑 Charging stopped")


def cmd_location(args):
    """Get vehicle location."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    
    data = vehicle.get_vehicle_data()
    drive = data['drive_state']
    
    lat, lon = drive['latitude'], drive['longitude']
    print(f"📍 Location: {lat}, {lon}")
    print(f"   https://www.google.com/maps?q={lat},{lon}")


def cmd_honk(args):
    """Honk the horn."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    vehicle.command('HONK_HORN')
    print("📢 Honked!")


def cmd_flash(args):
    """Flash the lights."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    vehicle.sync_wake_up()
    vehicle.command('FLASH_LIGHTS')
    print("💡 Flashed lights!")


def cmd_wake(args):
    """Wake up the vehicle."""
    tesla = get_tesla(args.email or os.environ.get("TESLA_EMAIL"))
    vehicle = get_vehicle(tesla)
    print("⏳ Waking vehicle...")
    vehicle.sync_wake_up()
    print("✅ Vehicle is awake")


def main():
    parser = argparse.ArgumentParser(description="Tesla vehicle control")
    parser.add_argument("--email", "-e", help="Tesla account email")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Auth
    subparsers.add_parser("auth", help="Authenticate with Tesla")
    
    # Status
    subparsers.add_parser("status", help="Get vehicle status")
    
    # Lock/unlock
    subparsers.add_parser("lock", help="Lock the vehicle")
    subparsers.add_parser("unlock", help="Unlock the vehicle")
    
    # Climate
    climate_parser = subparsers.add_parser("climate", help="Climate control")
    climate_parser.add_argument("action", choices=["on", "off", "temp"])
    climate_parser.add_argument("value", nargs="?", help="Temperature value")
    climate_parser.add_argument("--fahrenheit", "-f", action="store_true", default=True)
    
    # Charge
    charge_parser = subparsers.add_parser("charge", help="Charging control")
    charge_parser.add_argument("action", choices=["status", "start", "stop"])
    
    # Location
    subparsers.add_parser("location", help="Get vehicle location")
    
    # Honk/flash
    subparsers.add_parser("honk", help="Honk the horn")
    subparsers.add_parser("flash", help="Flash the lights")
    
    # Wake
    subparsers.add_parser("wake", help="Wake up the vehicle")
    
    args = parser.parse_args()
    
    commands = {
        "auth": cmd_auth,
        "status": cmd_status,
        "lock": cmd_lock,
        "unlock": cmd_unlock,
        "climate": cmd_climate,
        "charge": cmd_charge,
        "location": cmd_location,
        "honk": cmd_honk,
        "flash": cmd_flash,
        "wake": cmd_wake,
    }
    
    try:
        commands[args.command](args)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
