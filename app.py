from Helpers.packets_helper import *
from constants import *


parser = LogParser()


def main():
    with open(LAST_LOG_PATH) as f:
        parser.read(f)


if __name__ == "__main__":
    main()
