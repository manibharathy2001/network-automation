import difflib
import yaml
import os

# Load devices
with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

# Create reports folder if not exists
os.makedirs("reports", exist_ok=True)

for device in devices:
    print(f"\n🔍 Comparing {device['name']}")

    pre_file = f"logs/prelogs/{device['name']}_pre_sh_run_logs.txt"
    post_file = f"logs/postlogs/{device['name']}_post_sh_run_logs.txt"

    # Check if files exist
    if not os.path.exists(pre_file) or not os.path.exists(post_file):
        print(f"❌ Missing files for {device['name']}")
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

    # Save diff report
    report_file = f"reports/{device['name']}_diff.txt"

    with open(report_file, "w") as f:
        for line in diff:
            f.write(line + "\n")

    print(f"✅ Diff report saved: {report_file}")