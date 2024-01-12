# -*- coding: utf-8 -*-

import argparse

from common import *
from termgecko import TermGecko
# from libs import fs
from libs.config import Config
from tabs.Setting import SettingMenu


def main():
    parser = argparse.ArgumentParser(description='TermGecko')
    parser.add_argument('--DEBUG', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    termGecko = TermGecko(
        debug_mode=args.DEBUG
    )

    termGecko.init()

    while True:
        termGecko.proc()


if __name__ == '__main__':
    main()
