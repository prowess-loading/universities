import random

proxy_config = {
    "host": "7vfi6pj1.lunaproxy.net",
    "port": 12233,
    "username": "prowess_B6vvA",
    "password": "VU7mRaafTWhwd",

    "region": {
        "us": "us",
        "na": ["us", "ca"],
        "au": ["au", "nz"],
        "as": ["jp", "sg", "kr"],
        # "as": ["jp", "sg", "hk", "kr"],
        "eu": [
            "gb", "de", "fr", "it", "se", "be", "at", "es", "ie", "fi", "pt", "lv", "pl",
            "hu", "nl", "ch", "cz", "no", "is", "gr", "ua", "hr"
        ]
    }
}


def generate_proxy_with_region(region):
    regions = proxy_config["region"]
    selected_regions = []

    if region == "rd":
        selected_regions = [random.choice(
            sum([v if isinstance(v, list) else [v] for v in regions.values()], []))]
    else:
        region_keys = region.split(", ")
        for key in region_keys:
            if key in regions:
                selected_regions.extend(regions[key] if isinstance(
                    regions[key], list) else [regions[key]])

    selected_region = random.choice(selected_regions)

    if selected_region in regions["us"] or selected_region in regions["na"] or selected_region in regions["au"]:
        hostname_prefix = "na."
    elif selected_region in regions["as"]:
        hostname_prefix = "as."
    elif selected_region in regions["eu"]:
        hostname_prefix = "eu."
    else:
        hostname_prefix = "pr."

    host_with_prefix = f"{hostname_prefix}{proxy_config['host']}"
    proxy_string = f"https://user-{proxy_config['username']}-region-{selected_region}:{proxy_config['password']}@{host_with_prefix}:{proxy_config['port']}"

    return proxy_string
