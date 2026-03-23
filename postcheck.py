import yaml
from netmiko import ConnectHandler
import os

POSTCHECK_COMMANDS = [
    "show ip route",
    "show isis neighbor",
    "show mpls ldp neighbor"
]

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

os.makedirs("logs/postlogs", exist_ok=True)

for device in devices:
    print(f"Postcheck on {device['name']}")

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["ip"],
        username=device["username"],
        password=device["password"],
    )

    # 🔹 Post logs
    with open(f"logs/postlogs/{device['name']}_postlogs.txt", "w") as f:
        for cmd in POSTCHECK_COMMANDS:
            output = conn.send_command(cmd)
            f.write(f"\n===== {cmd} =====\n{output}\n")

    # 🔹 Running config
    run = conn.send_command("show running-config")
    with open(f"logs/postlogs/{device['name']}_post_sh_run_logs.txt", "w") as f:
        f.write(run)

    conn.disconnect()