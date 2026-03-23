import yaml
from netmiko import ConnectHandler
import os

PRECHECK_COMMANDS = [
    "show ip interface brief",
    "show ip route",
    "show isis neighbor",
    "show mpls ldp neighbor"
]

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

os.makedirs("logs/prelogs", exist_ok=True)

for device in devices:
    print(f"Precheck on {device['name']}")

    conn = ConnectHandler(**{
        "device_type": device["device_type"],
        "host": device["ip"],
        "username": device["username"],
        "password": device["password"],
    })

    # 🔹 Pre logs
    with open(f"logs/prelogs/{device['name']}_prelogs.txt", "w") as f:
        for cmd in PRECHECK_COMMANDS:
            output = conn.send_command(cmd)
            f.write(f"\n===== {cmd} =====\n{output}\n")

    # 🔹 Running config
    run = conn.send_command("show running-config")
    with open(f"logs/prelogs/{device['name']}_pre_sh_run_logs.txt", "w") as f:
        f.write(run)

    conn.disconnect()