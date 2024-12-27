import random
import time
from setup import utils
from data.utms import domain
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import threading
from datetime import datetime


class SmoothScroll:
    def __init__(self, driver, speed=50.0):
        self.driver = driver
        self.speed = speed

    def _scroll(self, scroll_amount, total_scroll_height):
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        next_position = min(
            max(0, current_position + scroll_amount), total_scroll_height)
        scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

        for position in range(int(current_position), int(next_position), int(scroll_step)):
            self.driver.execute_script(
                f"window.scrollTo(0, {min(position, total_scroll_height)});")
            time.sleep(0.03 + random.uniform(-0.03, 0.03))

        return self.driver.execute_script("return window.pageYOffset;")

    def _toggle_scroll_direction(self, scrolling_up, toggle_up_once):
        if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
            return True, True
        elif scrolling_up:
            return False, toggle_up_once
        return scrolling_up, toggle_up_once

    def _random_pause(self):
        if random.random() < 0.015:
            time.sleep(1 + random.uniform(0, 1))
        else:
            time.sleep(random.uniform(0.3, 0.6))

    def wait_for_element(driver, timeout=10):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(
                    f"Timeout reached: Could not find the target element within {timeout} seconds.")
                driver.quit()
                return False

    def scroll_to_single(self, target_selector, by=By.CSS_SELECTOR):
        try:
            target_element = self.driver.find_element(by, target_selector)
        except NoSuchElementException:
            print(f"Element with selector '{target_selector}' not found.")
            return

        scrolling_up = False
        toggle_up_once = False

        while True:
            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                time.sleep(3)
                try:
                    target_element.click()
                except Exception as e:
                    print(
                        f"Error: Element is not clickable or another issue occurred: {e}")
                break

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(400, 900)
            self._scroll(scroll_amount, self.driver.execute_script(
                "return document.body.scrollHeight"))

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

    def scroll_to_end(self):
        max_attempts = 4
        attempts = 0
        scrolling_up = False
        toggle_up_once = False
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        early_quit_threshold = random.uniform(
            0.3, 0.5) * total_scroll_height if random.random() < 0.4 else None

        while True:
            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(400, 800)
            new_position = self._scroll(scroll_amount, total_scroll_height)

            if early_quit_threshold and new_position >= early_quit_threshold:
                print(f"Early quitting...")
                self.driver.quit()
                break

            if new_position == current_position:
                attempts += 1
                if attempts >= max_attempts:
                    print("Scrolling stagnated. Exiting...")
                    break
            else:
                attempts = 0

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

            if new_position >= total_scroll_height - 1:
                print("Reached the end of the page.")
                break

    def scroll_to_ad_click(self, target_selector, quit_time, log_file, by=By.CSS_SELECTOR):
        ad_count_incremented = False
        self.driver_quit = False

        def quit_driver_after_timeout(driver, timeout):
            def quit_driver():
                print(f"Clicked at {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(timeout)

                if not self.driver_quit:
                    driver.quit()
                    self.driver_quit = True

                if not ad_count_incremented:
                    utils.increment_ad_click_count(log_file)
                print(f"Quit at {datetime.now().strftime('%H:%M:%S')}")

            thread = threading.Thread(target=quit_driver)
            thread.daemon = True
            thread.start()

        try:
            target_element = self.driver.find_element(by, target_selector)
        except NoSuchElementException:
            print("Element not found.")
            return

        scrolling_up = False
        toggle_up_once = False
        start_time = time.time()
        timeout = 25
        ad_timeout = 5

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(
                    f"Timeout reached: Could not find the target ad within {timeout} seconds.")
                if not self.driver_quit:
                    self.driver.quit()
                    self.driver_quit = True
                break

            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, target_selector))
                    )
                    height = self.driver.execute_script(
                        "return arguments[0].offsetHeight;", target_element)

                    if height > 10:
                        quit_driver_after_timeout(self.driver, ad_timeout)
                        target_element.click()
                    else:
                        self.scroll_to_end()
                        break

                    print(f"Will sleep for {quit_time} seconds.")
                    time.sleep(int(quit_time) - 1)

                    if not ad_count_incremented:
                        current_url = self.driver.current_url
                        if domain not in current_url:
                            utils.increment_ad_click_count(log_file)
                            print("Ad loaded and count increased.")
                            ad_count_incremented = True
                        else:
                            print("Could not click properly.")

                    if not self.driver_quit:
                        self.driver.quit()
                        self.driver_quit = True

                except TimeoutException:
                    if not self.driver_quit:
                        self.driver.quit()
                        self.driver_quit = True
                except Exception as e:
                    print(f"Clicked successfully in Thread")
                    if not self.driver_quit:
                        self.driver.quit()
                        self.driver_quit = True
                break

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(200, 500)
            self._scroll(scroll_amount, self.driver.execute_script(
                "return document.body.scrollHeight"))

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

    def scroll_bottom_up_ad_click(self, target_selector, quit_time, log_file, by=By.CSS_SELECTOR):
        scrolling_up = False
        toggle_once = False
        ad_count_incremented = False
        self.driver_quit = False

        def quit_driver_after_timeout(driver, timeout, log_file, ad_count_incremented):
            def quit_driver():
                print(
                    f"Clicked at {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(timeout)

                if not self.driver_quit:
                    driver.quit()
                    self.driver_quit = True

                if not ad_count_incremented:
                    utils.increment_ad_click_count(log_file)
                print(f"Quit at {datetime.now().strftime('%H:%M:%S')}")

            thread = threading.Thread(target=quit_driver)
            thread.daemon = True
            thread.start()

        # Phase 1: Scroll to the Bottom
        homepage_timeout = 20
        start_time_phase1 = time.time()

        while True:
            elapsed_time = time.time() - start_time_phase1
            if elapsed_time > homepage_timeout:
                print(
                    f"Timeout reached: Could not find the target ad within {timeout} seconds.")
                if not self.driver_quit:
                    self.driver.quit()
                    self.driver_quit = True
                break

            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            # Scroll downward
            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(500, 900)
            new_position = self._scroll(scroll_amount, total_scroll_height)

            if new_position == current_position:
                break

            scrolling_up, toggle_once = self._toggle_scroll_direction(
                scrolling_up, toggle_once)
            self._random_pause()

            if new_position >= total_scroll_height - 1:
                break

        # Phase 2: Scroll Upwards
        scrolling_up = True
        start_time_phase2 = time.time()
        timeout = 25
        ad_timeout = 15

        while True:
            elapsed_time = time.time() - start_time_phase2
            if elapsed_time > timeout:
                print(
                    f"Timeout reached: Could not find the target ad within {timeout} seconds.")
                if not self.driver_quit:
                    self.driver.quit()
                    self.driver_quit = True
                break

            target_element = self.driver.find_element(by, target_selector)
            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )

            if target_in_view:
                try:
                    height = self.driver.execute_script(
                        "return arguments[0].offsetHeight;", target_element)

                    if height > 10:
                        quit_driver_after_timeout(
                            self.driver, ad_timeout, log_file, ad_count_incremented)
                        target_element.click()
                    else:
                        break

                    print(f"Will sleep for {quit_time} seconds.")
                    time.sleep(int(quit_time) - 1)

                    if not ad_count_incremented:
                        current_url = self.driver.current_url
                        if domain not in current_url:
                            utils.increment_ad_click_count(log_file)
                            print("Ad loaded and count increased.")
                            ad_count_incremented = True
                        else:
                            print("Could not click properly.")

                    if not self.driver_quit:
                        self.driver.quit()
                        self.driver_quit = True

                except Exception as e:
                    print(f"Clicked successfully in Thread")
                    if not self.driver_quit:
                        self.driver.quit()
                        self.driver_quit = True
                break

            scroll_amount = random.randint(
                80, 150) if scrolling_up else -random.randint(300, 800)
            self._scroll(scroll_amount, total_scroll_height)

            scrolling_up, toggle_once = self._toggle_scroll_direction(
                scrolling_up, toggle_once)
            self._random_pause()
