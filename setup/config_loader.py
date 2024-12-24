import json
import logging


def load_config(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading {filename}: {e}")
        return {}
