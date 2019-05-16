from enum import Enum

HEADER = '\033[96m'
GREEN = '\033[92m'
SHOWSTOPPER = '\033[91m'
CRITICAL = '\033[93m'
ENDC = '\033[0m'
BOLD = '\033[1m'


class IconsEnum(Enum):
    ERROR, INFO, SUCCESS, UNICORN, WARNING = range(5)


def print_msg(icon, text):
    icons = {
        IconsEnum.INFO: HEADER + 'ℹ' + ENDC + BOLD,
        IconsEnum.SUCCESS: GREEN + '✔' + ENDC + BOLD,
        IconsEnum.WARNING: CRITICAL + '⚠' + ENDC + BOLD,
        IconsEnum.ERROR: SHOWSTOPPER + '✖' + ENDC + BOLD,
        IconsEnum.UNICORN: '🦄' + BOLD,
    }

    print(icons[icon], text, ENDC)
