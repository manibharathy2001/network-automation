import yaml
from netmiko import ConnectHandler
import os

# ADD LOGGING
from modules.logger import setup_logger
import logging

setup_logger()

POSTCHECK_COMMANDS = [
    "show ip route",
    "show isis neighbor",
    "show mpls ldp neighbor"
]

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

os.makedirs("logs/postlogs", exist_ok=True)

for device in devices:
    try:
        logging.info(f"Postcheck started for {device['name']}")

        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["ip"],
            username=device["username"],
            password=device["password"],
        )

        logging.info(f"Connected to {device['name']}")

        # Postcheck commands
        with open(f"logs/postlogs/{device['name']}_postlogs.txt", "w") as f:
            for cmd in POSTCHECK_COMMANDS:
                logging.info(f"Running '{cmd}' on {device['name']}")
                output = conn.send_command(cmd)
                f.write(f"\n===== {cmd} =====\n{output}\n")

        logging.info(f"Postcheck commands completed for {device['name']}")

        # Running config
        run = conn.send_command("show running-config")

        with open(f"logs/postlogs/{device['name']}_post_sh_run_logs.txt", "w") as f:
            f.write(run)

        logging.info(f"Post running-config saved for {device['name']}")

        conn.disconnect()

    except Exception as e:
        logging.error(f"Error during postcheck on {device['name']}: {e}")