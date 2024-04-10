import os
from dotenv import load_dotenv

load_dotenv()


def get_last_folder_by_path(path):
    if path is None:
        return None

    folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    if not folders:
        return None

    latest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(path, f)))
    return os.path.join(path, latest_folder)


LOGS_CONFIG_PATH = os.getenv("LOG_CONFIG_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")
LAST_LOG_PATH = os.path.join(get_last_folder_by_path(LOGS_PATH), "Power.log")

if LAST_LOG_PATH:
    print("Последняя папка с логами:", LAST_LOG_PATH)
else:
    print("Нет доступных папок с логами.")
