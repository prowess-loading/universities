import platform
import subprocess
import os
from datetime import datetime
from setup import utils
from multiprocessing import Pool


# def run_command(args):
#     """Run the command in a separate process."""
#     terminal_number, system_platform, working_directory, command = args

#     if system_platform == "Windows":
#         subprocess.Popen(
#             ["cmd", "/c", f"start cmd /c {command}"], shell=True
#         )

#     elif system_platform == "Darwin":
#         apple_script = f'''
#         tell application "Terminal"
#             do script "cd {working_directory} && {command}; exit"
#         end tell
#         '''
#         subprocess.Popen(["osascript", "-e", apple_script])

#     else:
#         subprocess.Popen(
#             ["gnome-terminal", "--", "bash", "-c",
#              f'{command}; exit; exec bash'])

def run_command(args):
    terminal_number, system_platform, working_directory, command = args

    if system_platform == "Windows":
        subprocess.Popen(
            ["cmd", "/c", f"start cmd /c {command}"], shell=True
        )
    elif system_platform == "Darwin":
        apple_script = f'''
        tell application "Terminal"
            do script "cd {working_directory} && {command}; exit"
            delay 0.5 -- Ensure the command starts before we proceed                
        end tell
        '''
        subprocess.Popen(["osascript", "-e", apple_script])
    else:
        subprocess.Popen(
            ["gnome-terminal", "--", "bash", "-c",
             f'{command}; exit; exec bash'])


def main():
    num_terminals = int(input("Enter the number of terminals to open: "))
    num_repetition = int(
        input("How many times do you want to run the test? (Max: 1000): "))

    # Create the log file when the run_university starts
    ad_click_log_file = utils.create_ad_click_log()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    terminal_log_file = f"log/terminal_run_log_{timestamp}.log"

    os.makedirs('log', exist_ok=True)

    # Prepare the command to execute
    system_platform = platform.system()
    working_directory = os.getcwd()

    # Original code (commented)
    """
    for i in range(num_terminals):
        terminal_number = i + 1
        if system_platform == "Windows":
            command = f"python main.py {num_repetition} {terminal_number} {ad_click_log_file} {terminal_log_file}"
            subprocess.Popen(
                ["cmd", "/c", f"start cmd /c {command}"], shell=True
            )

        elif system_platform == "Darwin":
            command = f"python3 main.py {num_repetition} {terminal_number} {ad_click_log_file} {terminal_log_file}"
            apple_script = f'''
            tell application "Terminal"
                do script "cd {working_directory} && {command}; exit"
                delay 0.5 -- Ensure the command starts before we proceed                
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script])

        else:
            command = f"python3 main.py {num_repetition} {terminal_number} {ad_click_log_file} {terminal_log_file}"
            subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c",
                 f'{command}; exit; exec bash'])
    """

    # New multiprocessing code
    with Pool(num_terminals) as pool:
        args = [
            (
                i + 1,
                system_platform,
                working_directory,
                f"{'python' if system_platform == 'Windows' else 'python3'} main.py {num_repetition} {i + 1} {ad_click_log_file} {terminal_log_file}"
            )
            for i in range(num_terminals)
        ]
        pool.map(run_command, args)


if __name__ == "__main__":
    main()
