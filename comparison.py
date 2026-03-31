import difflib
import yaml
import os

# ADD LOGGING
from modules.logger import setup_logger
import logging

setup_logger()

# Load devices
with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

# Create reports folder
os.makedirs("reports", exist_ok=True)

for device in devices:
    try:
        logging.info(f"Comparison started for {device['name']}")

        pre_file = f"logs/prelogs/{device['name']}_pre_sh_run_logs.txt"
        post_file = f"logs/postlogs/{device['name']}_post_sh_run_logs.txt"

        # Check files exist
        if not os.path.exists(pre_file) or not os.path.exists(post_file):
            logging.error(f"Missing files for {device['name']}")
            continue

        # Read files
        with open(pre_file) as f:
            pre = f.readlines()

        with open(post_file) as f:
            post = f.readlines()

        # Generate diff
        diff = difflib.unified_diff(
            pre,
            post,
            fromfile="pre_config",
            tofile="post_config",
            lineterm=""
        )

        report_file = f"reports/{device['name']}_diff.txt"

        with open(report_file, "w") as f:
            for line in diff:
                f.write(line + "\n")

        logging.info(f"Diff report created for {device['name']} → {report_file}")

    except Exception as e:
        logging.error(f"Comparison failed for {device['name']}: {e}")