import json
import random
from setup.smooth_scroll import SmoothScroll


class HomePage:
    def __init__(self, driver):
        self.driver = driver

        with open('data/page_locators.json', 'r') as f:
            self.locators = json.load(f)

        self.universities = [
            "Imperial-Collage-London",
            "Massachusetts-Institute-of-Technology",
            "University-of-Cambridge",
            # "University-of-Oxford",       # Not Added
            "Stanford-University",
            # "University-of-Zurich",
            "Harvard-University",
            # "National-University-of-Singapore",
            # "University-College-London",  # Not Added
            "California-Institute-of-Technology",
            # "University-of-Pennsylvania", # Not Added
            "University-of-California",
        ]

        self.selected_university_name = random.choice(self.universities)
        # self.selected_university_name = "Massachusetts-Institute-of-Technology"

    def open_university_page(self):
        university_page_article_id = self.locators["universities"].get(
            self.selected_university_name)
        print(f"Selected University: {self.selected_university_name}")

        navigator = SmoothScroll(self.driver)
        navigator.scroll_to_single(university_page_article_id)
