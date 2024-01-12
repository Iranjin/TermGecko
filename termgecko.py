# -*- coding: utf-8 -*-

import libs.fs as fs
from typing import Optional
from libs.language import Language
from libs.cmdparser import Command
from common import *
from libs.config import Config
from tabs.Menu import Menu
from time import sleep
from libs.language_codes import LANGUAGE_CODES

### Tabs ##########################
from tabs.Code import CodeMenu
from tabs.Exit import ExitMenu
from tabs.Help import HelpMenu
from tabs.Setting import SettingMenu
###################################


class TermGecko:
    def __init__(self, debug_mode: bool = False):
        # self.__init = False
        self.__debug_mode = debug_mode
        self.__tabs: list[Menu] = []
        self.__current_tab: Optional[Menu] = None
        self.__config = Config()
        self.__language = Language()
        # self.add_tab(*tabs)

    def add_menu(self, *tabs: Menu):
        for tab in tabs:
            self.__tabs.append(tab)

    def __check_language(self):
        def download_language(language_code: str):
            file_bin = fs.get_file(
                'https://raw.githubusercontent.com/Iranjin/TermGecko/main/languages/%s.lng' % (language_code))
            fs.File('languages/%s.lng' % (language_code)).write(file_bin)

        clear()

        language_code = self.__config.get('General', 'Language', 'ja_JP')
        if language_code not in LANGUAGE_CODES:
            print(' - Invalid language code' + (
                ' in \'' + self.__config.path +
                '\'' if self.__config.loaded and self.__config.path else ''
            ))
            return -1

        self.__config.save()

        folder = fs.Folder('languages/')
        language_files = folder.glob(r'.*\.lng')

        # 言語ファイルがあった場合
        if language_files:
            if language_code not in [file.name.rstrip('.lng') for file in language_files]:
                print(' - Language file \'%s.lng\' not found' %
                      (language_code))
                return -1
        else:
            print(' - Language file not found')
            sleep(1)
            print(' - Downloading language files...')

            if not folder.exists():
                folder.create()
                print(' - Created language folder')

            download_language(language_code)

            print(' - Success')
            sleep(2)
            clear()

        self.__language.load(os.path.join(folder.path, language_code + '.lng'))

        return 0

    def init(self):
        self.__config.load('config.ini')
        lang_status = self.__check_language()
        if lang_status != 0:
            exit()

        self.add_menu(
            CodeMenu(self.__config, self.__language),
            ExitMenu(self.__config, self.__language),
            HelpMenu(self.__config, self.__language),
            SettingMenu(self.__config, self.__language),
        )

        set_console_title('debug')

    # @property
    # def tabs(self):
    #     return self.__tabs

    # def add_tab(self, *tabs: Tab):

    #     for tab in tabs:
    #         self.__tabs.append(tab)

    def proc(self):
        clear()

        command = Command(
            arg1=(str, lambda x: any(
                [x.strip() in [key for key in tab.keys] for tab in self.__tabs]))
        )

        try:
            selected_tab = command.input('TermGecko%s > ' % (
                ('[DEBUG]' if self.__debug_mode else '')
            )).get('arg1')
        except ValueError:
            return
        else:
            if selected_tab.valid == False:
                return

        self.__current_tab = next(
            (tab for tab in self.__tabs if selected_tab.arg in tab.keys), None)

        while True:
            clear()
            status = self.__current_tab.run()
            if status == 0:
                break
