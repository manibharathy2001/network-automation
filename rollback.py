import yaml
from netmiko import ConnectHandler

# ADD LOGGING
from modules.logger import setup_logger
import logging

setup_logger()

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:
    try:
        logging.info(f"Rollback started for {device['name']}")

        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["ip"],
            username=device["username"],
            password=device["password"],
        )

        logging.info(f"Connected to {device['name']}")

        interface = device["interface"]

        # Step 1: Remove metric
        remove_cmds = [
            f"interface {interface}",
            "no isis metric"
        ]

        logging.info(f"Removing ISIS metric on {device['name']} ({interface})")
        conn.send_config_set(remove_cmds)

        # Step 2: Restore running config
        with open(f"logs/prelogs/{device['name']}_pre_sh_run_logs.txt") as f:
            config = f.read()

        logging.info(f"Restoring precheck configuration on {device['name']}")
        conn.send_config_set(config.splitlines())

        logging.info(f"Rollback completed successfully on {device['name']}")

        conn.disconnect()

    except Exception as e:
        logging.error(f"Rollback failed on {device['name']}: {e}")