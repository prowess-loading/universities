import random


def get_device(devices, device_name):

    device_name = random.choice(
        list(devices.keys())) if device_name == "random" else device_name

    device = devices.get(device_name)
    print(f"Device name: {device_name}")

    if not device:
        raise ValueError(
            f"Device '{device_name}' not found in the configuration file.")
    return device
