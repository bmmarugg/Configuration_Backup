import netmiko
import json
from datetime import date

with open("path/to/creds.json") as credentials:
    creds = json.load(credentials)

name = creds["username"]
passwrd = creds["passwrd"]
enablepw = creds["enablepw"]
local_user = creds["local_user"]
local_pass = creds["local_pass"]
ios = "cisco_ios"

with open("path/to/device_list.txt") as f:
    device_line = f.read().splitlines()
while("" in device_line):
    device_line.remove("")
device_list = device_line

today = date.today()
config_log = open("path/to/config_log_{}.txt"
                  .format(today), "w")

def main():

    try:
        connect = netmiko.ConnectHandler(username=name, password=passwrd, device_type=ios, ip=device, secret=enablepw)
        if ">" in connect.find_prompt():
            connect.enable()
        print("Now connected to: {}".format(device))

        device_config = open("path/to/config/repo/{}_{}-running_config.txt".format(today, device), 'w')

        connect.send_command("term len 0")
        run_config = connect.send_command("sh run")
        device_config.write(run_config)

        config_log.write("Successfully pulled running config for: {}".format(device))

    except:
        print("Could not connect to {} using domain creds. Trying local creds now... ".format(device))

    try:
        connect = netmiko.ConnectHandler(username=local_user, password=local_pass, device_type=ios, ip=device,
                                         secret=enablepw)
        if ">" in connect.find_prompt():
            connect.enable()
        print("Now connected to: {}".format(device))
        device_config = open("path/to/config/repo/{}_{}-running_config.txt".format(today, device), 'w')

        connect.send_command("term len 0")
        run_config = connect.send_command("sh run")
        device_config.write(run_config)
        config_log.write("Running-config for: {} pulled successfully.".format(device))

    except:
        print("Could not connect to {}. Moving on...".format(device))
        config_log.write("Could NOT pull running-config for: {}. Check device connectivity or enable password"
                         .format(device))


def fw_main():
    try:
        connect = netmiko.ConnectHandler(username=local_user, password=local_pass, device_type=ios, ip=device,
                                         secret=enablepw)
        if ">" in connect.find_prompt():
            connect.enable()
        print("Now connected to: {}".format(device))
        device_config = open("path/to/config/repo/{}_{}-running_config.txt".format(today, device), 'w')

        connect.send_command("term pager 0")
        run_config = connect.send_command("sh run")
        device_config.write(run_config)
        config_log.write("Running-config for: {} pulled successfully.".format(device))

    except:
        print("Could not connect to {}. Moving on...".format(device))
        config_log.write("Could NOT pull running-config for: {}. Check device connectivity or enable password"
                         .format(device))



for device in device_list:
    if "fw" not in device.lower() or "asa" not in device.lower():
        main()
    else:
        fw_main()