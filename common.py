# -*- coding: utf-8 -*-

import platform
import os
import sys
import re


def set_console_title(title: str): ...
# sys.stdout.write('\033]0;%s\007' % (title))
# sys.stdout.flush()


def digit_count(decimal: int, base: int = 10):
    count = 0
    while decimal != 0:
        decimal //= base
        count += 1
    return count


def is_valid_ip_address(ip_address: str) -> bool:
    return re.match(r'^192\.168\.\d{1,3}\.\d{1,3}$', ip_address) is not None


def remove_white_space(string_: str):
    for white_space in ' \t\n\r\v\f':
        string_ = string_.replace(white_space, '')
    return string_


def clear():
    os_name = platform.platform()
    if 'Windows' in os_name:
        os.system('cls')
    elif 'macOS' in os_name or 'Linux' in os_name:
        os.system('clear')
    else:
        print('\n' * 99)

    # os_system = platform.system()

    # if os_system == 'Windows':
    #     os.system('cls')
    # elif os_system == 'Linux' or os_system == 'Darwin':
    #     os.system('clear')
    # else:
    #     print('\n' * 100)

    # system_platform = platform.system()
    # input(system_platform)

    # if system_platform == 'Windows':
    #     os.system('cls')
    # elif system_platform == 'Darwin':
    #     os.system('clear')
    # elif system_platform == 'Linux':
    #     os.system('clear')
    # elif system_platform == 'iOS':
    #     print('\n' * 100)
    # elif system_platform == 'Android':
    #     os.system('clear')
    # else:
    #     # print('Clearing console not supported on \'%s\'' % (system_platform))
    #     print('\n' * 100)
