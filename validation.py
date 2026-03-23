import yaml
from netmiko import ConnectHandler

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]


def check_isis(output):
    return "UP" in output.upper()


def check_mpls(output):
    return "OPERATIONAL" in output.upper() or "UP" in output.upper()


def check_routes(output):
    return "Gateway" in output or "via" in output


for device in devices:
    print(f"\n🔍 Validating {device['name']}")

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["ip"],
        username=device["username"],
        password=device["password"],
    )

    isis = conn.send_command("show isis neighbor")
    route = conn.send_command("show ip route")
    mpls = conn.send_command("show mpls ldp neighbor")

    isis_ok = check_isis(isis)
    route_ok = check_routes(route)
    mpls_ok = check_mpls(mpls)

    print(f"ISIS OK: {isis_ok}")
    print(f"ROUTE OK: {route_ok}")
    print(f"MPLS OK: {mpls_ok}")

    if isis_ok and route_ok and mpls_ok:
        print(f"✅ {device['name']} HEALTHY")

    else:
        print(f"❌ {device['name']} ISSUE DETECTED → Rollback required")

    conn.disconnect()