import random
from setup.config_loader import load_config
from setup.device_manager import get_device
from setup.browser_init import get_browser_options, initialize_driver
from setup import utils
from data import proxies

SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]


class BrowserSetup:
    def __init__(self):
        self.devices = load_config("data/devices.json")
        self.browser_deltas = load_config("data/browser_deltas.json")

    def setup_browser(self,
                      device_type,
                      proxy_active,
                      device_name,
                      browser_name,
                      region):

        proxy = proxies.generate_proxy_with_region(region)

        browser_name = browser_name if browser_name != "random" else random.choices(
            SUPPORTED_BROWSERS, weights=[80, 10, 10], k=1)[0]
        print(f"Browser name: {browser_name}")

        if device_type == "desk":
            user_agent = utils.get_desk_user_agent()
            options = get_browser_options(
                browser_name, user_agent, device_type)
            driver = initialize_driver(
                device_type, browser_name, options, proxy_active, proxy)
            return driver

        else:
            device = get_device(self.devices, device_name)
            user_agent = utils.get_mobile_user_agent(
                device, browser_name)
            adjusted_width, adjusted_height = utils.adjust_dimensions(
                device, self.browser_deltas, browser_name)
            options = get_browser_options(
                browser_name, user_agent, device_type, device)
            driver = initialize_driver(
                device_type, browser_name, options, proxy_active, proxy, adjusted_width, adjusted_height)
            utils.set_window_size(
                driver, device, self.browser_deltas, browser_name)
            return driver
