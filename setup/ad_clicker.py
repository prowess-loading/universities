import random
from selenium.webdriver.common.by import By
from setup.smooth_scroll import SmoothScroll
from selenium.webdriver.support.ui import WebDriverWait


class AdClicker:
    def __init__(self, driver):
        self.driver = driver

    def get_primary_ads(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "div[class^='code-block code-block-']")

        primary_visible_ads = []

        for element in elements:
            height = self.driver.execute_script(
                "return arguments[0].offsetHeight;", element)

            if height > 0:
                class_name = element.get_attribute('class')
                css_selector = f".{class_name.replace(' ', '.')}"
                primary_visible_ads.append(css_selector)

        return primary_visible_ads

    def get_side_ads(self):
        asides = self.driver.find_elements(
            By.CSS_SELECTOR, "#right-sidebar aside")

        side_ads = []
        for aside in asides:
            id_attribute = aside.get_attribute('id')
            class_attribute = aside.get_attribute('class')
            height = self.driver.execute_script(
                "return arguments[0].offsetHeight;", aside)

            if height > 10 and id_attribute.startswith('block-') and 'widget_search' not in class_attribute:
                css_selector = f"aside#{id_attribute} > div"
                side_ads.append(css_selector)

        return side_ads

    def select_random_ad(self, log_file, ad_target):
        smooth_scroll = SmoothScroll(self.driver)

        primary_visible_ads = self.get_primary_ads()

        if random.random() < 0.2:  # 20% chance
            side_ads = self.get_side_ads()
            all_ads = primary_visible_ads + side_ads
        else:
            all_ads = primary_visible_ads

        if not all_ads:
            print("No visible ad found")
            return None

        selected_ad = random.choice(all_ads)
        print(f"Selected ad: {selected_ad}")
        random_timeout = random.randint(2, 5)

        try:
            if ad_target == "homepage":
                smooth_scroll.scroll_bottom_up_ad_click(
                    selected_ad, random_timeout, log_file)
            else:
                smooth_scroll.scroll_to_ad_click(
                    selected_ad, random_timeout, log_file)

        except Exception as e:
            print(f"Error occurred while scrolling to ad and clicking: {e}")
