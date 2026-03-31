import yaml
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import time

# 🔹 Logging
from modules.logger import setup_logger
import logging

setup_logger()

# 🔹 Load devices
with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

# 🔹 Load template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("isis_metric.j2")

# 🔹 Deploy loop
for device in devices:
    try:
        logging.info(f"Deploy started for {device['name']}")

        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["ip"],
            username=device["username"],
            password=device["password"],
            global_delay_factor=2   # 🔥 handle slow response
        )

        logging.info(f"Connected to {device['name']}")

        # 🔹 Render config
        config = template.render(
            interface=device["interface"],
            metric=device["metric"]
        )

        # 🔹 Push config
        conn.send_config_set(
            config.splitlines(),
            delay_factor=2
        )

        time.sleep(1)  # stabilize CLI

        logging.info(f"Config pushed successfully on {device['name']}")

        # FIXED SAVE CONFIG (GNS3 safe)
        conn.send_command_timing("write memory")

        logging.info(f"Configuration saved on {device['name']}")

        conn.disconnect()
        logging.info(f"Disconnected from {device['name']}")

    except Exception as e:
        logging.error(f"Error on {device['name']}: {e}")