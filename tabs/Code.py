# -*- coding: utf-8 -*-

from .Menu import Menu
from libs.config import Config
from libs.language import Language
from common import *
from libs.codes import Code, Codes


class CodeMenu(Menu):
    def __init__(self, config: Config, language: Language):
        super().__init__(
            title='CodeMenu',
            description='code manager',
            keys=('l')
        )
        self.__config = config
        self.__language = language
        self.__codes: Code = []

    def run(self, **kwargs):
        input(self.__language['code_menu'])
        return 0
