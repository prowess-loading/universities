from setup.smooth_scroll import SmoothScroll
from setup import utils


class UniversityDetails:
    def __init__(self, driver, selected_university):
        self.driver = driver
        self.selected_university = selected_university

    def scroll_university_details_page(self):
        navigator = SmoothScroll(self.driver)
        navigator.scroll_to_end()
        utils.ensure_browser_quit(self.driver)
