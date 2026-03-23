import yaml
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("isis_metric.j2")

for device in devices:
    print(f"Deploying to {device['name']}")

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["ip"],
        username=device["username"],
        password=device["password"],
    )

    config = template.render(
        interface=device["interface"],
        metric=device["metric"]
    )

    conn.send_config_set(config.splitlines())
    conn.disconnect()