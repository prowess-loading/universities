import time
import sys
from setup.main_executor import MainExecutor
from setup import utils
import random


def main():

    num_tests = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    terminal_number = int(sys.argv[2]) if len(
        sys.argv) > 2 else 1
    ad_click_log_file = sys.argv[3] if len(
        sys.argv) > 3 else "log/default_ad_click_log.log"
    terminal_log_file = sys.argv[4] if len(
        sys.argv) > 4 else "log/default_terminal_log.log"

    executor = MainExecutor()

    for i in range(1, num_tests + 1):
        start_time = time.time()
        print(f"\nTerminal {terminal_number}: Running test #{i}...\n")
        driver = None

        click_ad = utils.should_click_ad(
            i, interval=executor.ad_click_frequency
        ) if executor.enable_ad_click else False

        if executor.device_type == "both":
            executor.device_type = random.choice(["desk", "mobile"])

        try:
            driver = executor.setup_driver()
            executor.process_run(
                driver, click_ad, ad_click_log_file)

        finally:
            utils.ensure_browser_quit(driver)

            duration = time.time() - start_time
            print(
                f"Terminal {terminal_number}: Test #{i} completed in {duration:.2f}s.")
            utils.log_to_file(terminal_number, i, duration, terminal_log_file)


if __name__ == "__main__":
    main()
