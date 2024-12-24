from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_browser_options(browser_name,
                        user_agent,
                        device_type,
                        device=None):

    options = {
        "chrome": ChromeOptions,
        "edge": EdgeOptions,
        "firefox": FirefoxOptions
    }[browser_name]()

    if device_type == "desk":
        if browser_name in ["chrome", "edge"]:
            options.add_argument(f'--user-agent={user_agent}')
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")

        elif browser_name == "firefox":
            options.set_preference("general.useragent.override", user_agent)

        return options

    else:
        if browser_name in ["chrome", "edge"]:
            options.add_experimental_option("mobileEmulation", {
                "userAgent": user_agent,
                "deviceMetrics": device["deviceMetrics"]
            })
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")

        elif browser_name == "firefox":
            options.set_preference("general.useragent.override", user_agent)

        return options


def initialize_driver(device_type, browser_name, options, proxy_active, proxy, width=None, height=None):

    if proxy_active:
        seleniumwire_options = {
            "proxy": {"http": proxy, "https": proxy}} if proxy else None

        if browser_name == "safari":
            if device_type == "desk":
                driver = webdriver.Safari(service=SafariService())
                return driver
            else:
                driver = webdriver.Safari(service=SafariService())
                driver.set_window_size(width, height)
                return driver

        return {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge,
        }[browser_name](options=options, seleniumwire_options=seleniumwire_options)

    else:
        if browser_name == "safari":
            if device_type == "desk":
                driver = webdriver.Safari(service=SafariService())
                return driver
            else:
                driver = webdriver.Safari(service=SafariService())
                driver.set_window_size(width, height)
                return driver

        return {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge,
        }[browser_name](options=options)
