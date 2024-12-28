import time
import sys
from multiprocessing import Process, Manager
from setup.main_executor import MainExecutor
from setup import utils
import psutil  # type: ignore
import random


def run_instance(terminal_number, i, ad_click_log_file, terminal_log_file, status_dict):
    start_time = time.time()
    print(f"\nTerminal {terminal_number}: Running test #{i}...\n")

    executor = MainExecutor()
    driver = None

    click_ad = utils.should_click_ad(
        i, interval=executor.ad_click_frequency
    ) if executor.enable_ad_click else False

    if executor.device_type == "both":
        executor.device_type = random.choice(["desk", "mobile"])

    try:
        driver = executor.setup_driver()
        status_dict["pid"] = driver.service.process.pid
        executor.process_run(driver, click_ad, ad_click_log_file)

    finally:
        utils.ensure_browser_quit(driver)
        duration = time.time() - start_time
        print(
            f"Terminal {terminal_number}: Test #{i} completed in {duration:.2f}s.")
        utils.log_to_file(terminal_number, i, duration, terminal_log_file)
        status_dict["status"] = "completed"


def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass
    except Exception as e:
        print(f"Error killing process tree with PID {pid}")


def main():
    num_tests = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    terminal_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    ad_click_log_file = sys.argv[3] if len(
        sys.argv) > 3 else "log/default_ad_click_log.log"
    terminal_log_file = sys.argv[4] if len(
        sys.argv) > 4 else "log/default_terminal_log.log"

    for i in range(1, num_tests + 1):
        status_dict = Manager().dict({"status": "running", "pid": None})

        process = Process(target=run_instance, args=(
            terminal_number, i,  ad_click_log_file, terminal_log_file, status_dict
        ))

        process.start()
        process.join(timeout=200)

        if process.is_alive():
            print(
                f"Terminal {terminal_number}: Test #{i} exceeded 250 seconds. Terminating...")
            process.terminate()
            process.join()

            driver_pid = status_dict.get("pid")
            if driver_pid:
                print(
                    f"Cleaning up browser for test #{i} with WebDriver PID {driver_pid}.")
                kill_process_tree(driver_pid)
            else:
                pass
        else:
            pass

        process.close()


if __name__ == "__main__":
    main()
