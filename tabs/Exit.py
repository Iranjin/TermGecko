# -*- coding: utf-8 -*-

from .Menu import Menu
from libs.config import Config
from libs.language import Language
from common import *
from libs.cmdparser import Command


class ExitMenu(Menu):
    def __init__(self, config: Config, language: Language,):
        super().__init__(
            title='Exit',
            description='Exit TermGecko',
            keys=('e', 'exit')
        )
        self.__config = config
        self.__language = language

    def run(self, **kwargs):
        command = Command(
            yes_or_no=(str, lambda x: x.lower() in ['y', 'n', 'yes', 'no'])
        )

        try:
            print('[%s]\ny: %s\nn: %s' % (self.__language['exit'], self.__language['yes'], self.__language['no']))
            yes_or_no = command.input('\n' + self.__language['exit_confirm'] + ' (y/n) > ').get('yes_or_no')
        except ValueError:
            return
        else:
            if yes_or_no.valid == False:
                return -1

        arg = yes_or_no.arg.lower()

        if arg in ['y', 'yes']:
            clear()
            exit()
        elif arg in ['n', 'no']:
            return 0
