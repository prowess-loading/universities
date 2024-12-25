import sys
from setup.browser_setup import BrowserSetup
from pages.homepage import HomePage
from pages.university_details import UniversityDetails
import random
from setup import utils
from setup.ad_clicker import AdClicker


class MainExecutor:
    def __init__(
            self, device_type="both",
            proxy_active=True,
            device_name="random",
            browser_name="random",
            region="na",                    # rd, us, na, au, as, eu
            add_utm=True,
            enable_ad_click=True,
            ad_click_frequency=7
    ):
        self.device_type = device_type
        self.proxy_active = proxy_active
        self.device_name = device_name
        self.browser_name = browser_name
        self.region = region
        self.add_utm = add_utm
        self.enable_ad_click = enable_ad_click
        self.ad_click_frequency = ad_click_frequency

    def setup_driver(self):
        browser_setup = BrowserSetup()
        return browser_setup.setup_browser(
            self.device_type,
            self.proxy_active,
            device_name=self.device_name,
            browser_name=self.browser_name,
            region=self.region,
        )

    def process_run(self, driver, click_ad, ad_log_file):

        target_url = utils.target_url(self.add_utm)
        utils.open_url_with_retry(driver, target_url)

        homepage = HomePage(driver)
        university_page = UniversityDetails(
            driver, homepage.selected_university_name)
        ad_clicker = AdClicker(driver)

        if click_ad:
            ad_target = random.choice(["homepage", "university_page"])
            # ad_target = "homepage"
            if ad_target == "homepage":
                print("Visiting Homepage")
                ad_clicker.select_random_ad(ad_log_file, ad_target)
            else:
                print("Visiting Homepage & University Page")
                homepage.open_university_page()
                ad_clicker.select_random_ad(ad_log_file, ad_target)
        else:
            homepage.open_university_page()
            university_page.scroll_university_details_page()
