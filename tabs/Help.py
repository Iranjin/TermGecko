# -*- coding: utf-8 -*-

from .Menu import Menu
from libs.config import Config
from libs.language import Language
from common import *
from libs.cmdparser import Command


class HelpMenu(Menu):
    def __init__(self, config: Config, language: Language):
        super().__init__(
            title='Help',
            description='Help menu',
            keys=('h', 'help')
        )
        self.__config = config
        self.__language = language

    def run(self, **kwargs):
        input('ヘルプメニュー')
        return 0
