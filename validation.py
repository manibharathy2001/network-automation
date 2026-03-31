import yaml
from netmiko import ConnectHandler
import subprocess
import sys

# Logging
from modules.logger import setup_logger
import logging

setup_logger()

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]


def check_isis(output):
    return "UP" in output.upper()


def check_mpls(output):
    return "OPERATIONAL" in output.upper() or "UP" in output.upper()


def check_routes(output):
    return "via" in output or "Gateway" in output


rollback_required = False  # GLOBAL FLAG

for device in devices:
    try:
        logging.info(f"Validation started for {device['name']}")

        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["ip"],
            username=device["username"],
            password=device["password"],
            global_delay_factor=2
        )

        logging.info(f"Connected to {device['name']}")

        # Collect outputs
        isis = conn.send_command("show isis neighbor")
        route = conn.send_command("show ip route")
        mpls = conn.send_command("show mpls ldp neighbor")

        # Checks
        isis_ok = check_isis(isis)
        route_ok = check_routes(route)
        mpls_ok = check_mpls(mpls)

        logging.info(f"{device['name']} ISIS OK: {isis_ok}")
        logging.info(f"{device['name']} ROUTE OK: {route_ok}")
        logging.info(f"{device['name']} MPLS OK: {mpls_ok}")

        if isis_ok and route_ok and mpls_ok:
            logging.info(f"{device['name']} HEALTHY ✅")
        else:
            logging.error(f"{device['name']} ISSUE DETECTED ❌")
            rollback_required = True  # mark failure

        conn.disconnect()

    except Exception as e:
        logging.error(f"Error during validation on {device['name']}: {e}")
        rollback_required = True


# AFTER ALL DEVICES CHECKED
if rollback_required:
    logging.error("Validation failed! Starting rollback...")

    subprocess.run(["python", "rollback.py"])

    logging.info("Rollback execution completed")

    sys.exit(1)   # FAIL STATUS

else:
    logging.info("Validation successful. No rollback required.")

    sys.exit(0)   # SUCCESS