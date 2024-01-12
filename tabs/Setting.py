# -*- coding: utf-8 -*-

from typing import Any, Optional, Callable
from libs.config import Config
from libs.language import Language
from libs.cmdparser import Command
# from libs.language_codes import LANGUAGE_CODES
from common import *
from .Menu import Menu
from common import *
from time import sleep


class Setting:
    def __init__(
        self,
        title: str,
        description: str,
        language: Language,
        setting_type: type,
        config: Config,
        section: str,
        key: str,
        default_value: Optional[Any] = None,
        restart_required: bool = False,
        formula: Optional[Callable[[Any], bool]] = None,
    ):
        # if setting_type not in (bool, int, float, str, list):
        #     raise ValueError('Invalid setting type. Allowed types are (bool, int, float, str)')

        # NOTE 継承するため全てProtected
        self._title = title
        self._description = description
        self._language = language
        self._setting_type = setting_type
        self._config = config
        self._section = section
        self._key = key
        self._default_value = default_value
        self._restart_required = restart_required
        self._formula = formula
        self._changed = False

        # TODO 短くする
        if self._section in self._config and self._key in self._config[self._section]:
            self._data = self._config[self._section][self._key]
        else:
            self._data = self._default_value

    @classmethod
    def get_type_str(cls, language: Language, type_: type):
        type_str = {
            bool: language['boolean'],
            str: language['string'],
            float: language['float'],
            int: language['integer']
        }
        return type_str.get(type_)

    @property
    def restart_required(self):
        return self._restart_required and self._changed

    def run(self, **kwargs):
        type_ = self._setting_type

        if type_ == bool:
            self._config.setdefault(self._section, {})
            self._config[self._section].setdefault(
                self._key, self._default_value)
            value = not self._config[self._section][self._key]
            self._config[self._section][self._key] = value
            self._data = value
        else:
            while True:
                default_value = self._default_value
                if default_value is None:
                    pass
                elif isinstance(default_value, str):
                    default_value = '\'' + default_value + '\''
                elif isinstance(default_value, bool):
                    default_value = 'ON' if default_value else 'OFF'
                elif isinstance(default_value, (int, float)):
                    default_value = str(default_value)
                # else:
                #     raise TypeError('Type \'%s\' is not supported' % (type(default_value)))

                clear()

                print('[%s]\n%s\n' % (self._title, self._description), end='')
                if self._default_value is None:
                    print()
                else:
                    print('%s: %s\n' % (self._language['default'], default_value))

                try:
                    result = Command(arg1=type_).input('%s > ' % (
                        self.get_type_str(self._language, type_)), True)
                except ValueError:
                    continue

                if result is None:
                    return -1

                value = result.get('arg1')

                if self._formula is not None:
                    try:
                        if not self._formula(value.arg):
                            value.valid = False
                    except TypeError:
                        print(' - ' + self._language['incorrect_type'])
                        value.valid = False

                if value.valid == False:
                    print(' - ' + self._language['format_is_incorrect'])
                    sleep(1)
                    continue

                self._config.setdefault(self._section, {self._key: None})
                self._config[self._section][self._key] = value.arg

                self._data = value.arg
                break
            clear()

        self._changed = True

        return 0

    @property
    def state(self):
        return self._data

    @property
    def description(self):
        return self._description

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._setting_type


class ListSetting(Setting):
    def __init__(
        self,
        title: str,
        description: str,
        language: Language,
        choices: list[Any],
        config: Config,
        section: str,
        key: str,
        default_value: Optional[int] = None,
        restart_required: bool = False,
    ):
        super().__init__(
            title=title,
            description=description,
            setting_type=str,
            config=config,
            section=section,
            key=key,
            # default_value=default_value,
            restart_required=restart_required,
            language=language
        )
        self._choices = choices
        self._default_value = default_value

    def run(self, **kwargs):
        while True:
            clear()

            print('[%s]' % (self._title))

            for i, choice in enumerate(self._choices):
                if isinstance(choice, str):
                    choice = '\'' + choice + '\''
                else:
                    choice = str(choice)
                print('%s │ %s' % (
                    str(len(self._choices) - i).ljust(digit_count(len(self._choices))),
                    choice
                ))

            print('\n' + self._description)

            if self._default_value is None:
                print()
            else:
                print('%s: \'%s\'\n' % (self._language['default'], self._choices[self._default_value]))

            command = Command(
                index=(int, lambda i: i - 1 in range(len(self._choices))))
            try:
                result = command.input('%s > ' % (self._language['select_an_index']), True)
            except ValueError:
                continue
            if result is None:
                return -1

            value = result.get('index')

            self._config.setdefault(self._section, {self._key: None})
            value_ = self._choices[len(self._choices) - value.arg]
            self._config[self._section][self._key] = value_
            self._data = value_
            break

        clear()
        self._changed = True
        return 0


# -----------------------------------


class SettingMenu(Menu):
    def __init__(self, config: Config, language: Language):
        super().__init__(
            title='Settings',
            description='Settings menu',
            keys=('s', 'setting', 'settings')
        )
        self.__config = config
        self.__language = language

        # NOTE 設定リスト
        # CHECK
        self.__settings = [
            Setting(language['ip_address'], language['enter_ip_address'], language, str, config, 'TCPGecko', 'IPAddress', '192.168.0.0',
                    formula=lambda x: is_valid_ip_address(x)),
            Setting(language['port'], language['enter_port'], language, int, config, 'TCPGecko', 'Port', 7331,
                    formula=lambda x: 0 <= x <= 65535),
            # Setting('Bool example', 'example description', language, bool, config, 'General', 'BoolExample', False),
            Setting(language['codelist_path'], language['enter_path'], language, str, config, 'General', 'CodeListPath', 'code_list.txt'),
            ListSetting(language['language'], language['select_language'], language, ['ja_JP', 'en_US'], config, 'General', 'Language', 0,
                        restart_required=True),
        ]

        Setting(language['port'], language['enter_port'], language, int, config, 'TCPGecko', 'Port', 7331,
                formula=lambda x: 0 <= x <= 65535),

    def run(self, **kwargs):
        clear()

        print('[%s]' % (self.__language['settings']))

        if self.__settings == []:
            print(' - ' + self.__language['no_settings'])
            sleep(2)
            return 0

        for i, setting in enumerate(self.__settings):
            print('%s │ %s' % (
                str(len(self.__settings) - i).ljust(digit_count(len(self.__settings))),
                setting.title
            ), end='')

            state = setting.state
            if isinstance(setting.state, str):
                state = '\'' + str(state) + '\''
            elif isinstance(setting.state, bool):
                state = 'ON' if state else 'OFF'
            else:
                state = str(state)

            print(': ' + state)

        restart_required_list: list[Setting] = []
        for setting in self.__settings:
            if setting.restart_required:
                restart_required_list.append(setting)

        if restart_required_list != []:
            print('\n - %s: %s' % (self.__language['restart_required'], ','.join(['\'' + setting.title + '\'' for setting in restart_required_list])))

        command = Command(
            index=(int, lambda i: i - 1 in range(len(self.__settings))))
        try:
            result = command.input('\n' + self.__language['select_an_index'] + ' > ', True)
        except ValueError:
            return 1
        if result is None:
            return 0

        index = result.get('index')

        if index.valid == False:
            return -1

        setting: Setting = self.__settings[len(self.__settings) - index.arg]
        status = setting.run()

        if status == 0:
            self.__config.save()
            clear()

            state = setting.state
            if isinstance(setting, str):
                state = '\'' + state + '\''
            elif isinstance(setting.state, bool):
                state = 'ON' if state else 'OFF'
            else:
                state = str(state)

            print(' - ' + self.__language['changed_to'] % (setting.title, state))
            sleep(1)
