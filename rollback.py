import yaml
from netmiko import ConnectHandler

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:
    print(f"\n🔄 Rollback on {device['name']}")

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["ip"],
        username=device["username"],
        password=device["password"],
    )

    # 🔹 Step 1: Remove metric (IMPORTANT)
    interface = device["interface"]

    remove_cmds = [
        f"interface {interface}",
        "no isis metric",
    ]

    print("Removing applied config...")
    conn.send_config_set(remove_cmds)

    # 🔹 Step 2: Restore original config
    with open(f"logs/prelogs/{device['name']}_pre_sh_run_logs.txt") as f:
        config = f.read()

    print("Restoring original config...")
    conn.send_config_set(config.splitlines())

    print("✅ Rollback completed")

    conn.disconnect()