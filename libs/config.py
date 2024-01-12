# -*- coding: utf-8 -*-

import os
import re
from typing import Union, Any, Optional


class Config:
    def __init__(self):
        self.__path = None
        self.__encoding = None
        self.__data = None

    def __detect_encoding(self, path: str):
        # TODO 種類が少ない
        encodings = [
            'utf-8',
            'cp932',
            'utf-16',
            'ascii',
        ]
        with open(path, 'rb') as f:
            file_bin = f.read()
        for encoding in encodings:
            try:
                file_bin.decode(encoding)
            except UnicodeDecodeError:
                pass
            else:
                return encoding
        return None

    # def __section_error(self, section_name: str):-
    #     raise KeyError('Invalid or missing %s section in the file.' % (section_name))

    @property
    def path(self):
        return self.__path

    @property
    def loaded(self):
        return self.__data is not None

    def load(self, path: str, encoding: Optional[str] = None):
        if not os.path.exists(path):
            # raise FileNotFoundError('File \'%s\' not found' % (path))
            with open(path, 'w') as f:
                pass

        self.__path = path
        if encoding is None:
            encoding = self.__detect_encoding(path)
        self.__encoding = encoding

        with open(self.__path, 'r', encoding=self.__encoding) as f:
            content = f.read()

        result: dict[str, dict[str, str]] = {}

        current_section = None
        for line in content.splitlines():
            line = line.strip()

            if line.startswith('[') and line.endswith(']'):
                current_section = line.lstrip('[').rstrip(']')

            elif '=' in line:
                if current_section is None:
                    raise SyntaxError('Section is not set')

                item = line.split('=')

                key = item[0]
                value = item[1]

                type_ = None

                if re.match(r'^-?\d+(?:\.\d+)?$', value):
                    type_ = float if '.' in value else int
                elif type_ is None and value.lower() in ('true', 'false'):
                    type_ = bool

                if value.startswith(('"', '\'')) and value.endswith(('"', '\'')):
                    value = value.strip('" \'')
                elif type_ is not None:
                    if type_ == bool:
                        value = value.lower() == 'true'
                    else:
                        value = type_(value)
                else:
                    raise TypeError(
                        'Unable to determine \'%s\' type' % (value))

                result.setdefault(current_section, {})
                result[current_section][key] = value

        self.__data = result

    def to_ini_format(self):
        result = ''
        for section, keys in self.__data.items():
            result += '[%s]\n' % (section)
            for key, value in keys.items():
                if isinstance(value, str):
                    value = '"%s"' % (value)
                result += '%s=%s\n' % (key, value)
            result += '\n'
        result = result.rstrip('\n')
        return result

    def to_dict(self):
        return self.__data

    def save(self):
        result = self.to_ini_format()
        if self.__path is None:
            raise Exception('Configuration is not loaded')
        with open(self.__path, 'w', encoding=self.__encoding) as f:
            f.write(result)

    def get(
        self,
        section: str,
        key: str,
        default_value: Optional[Union[str, int, float, bool]] = None
    ):
        keys = self.__data.get(section)
        if keys is None:
            if default_value is not None:
                self.__data.setdefault(section, {key: default_value})
            return default_value
        value = keys.get(key)
        if value is None:
            if default_value is not None:
                self.__data[section].setdefault(key, default_value)
            return default_value
        return value

    def setdefault(self, key: Any, value: Optional[Any] = None):
        self.__data.setdefault(key, value)

    def __getitem__(self, key: str):
        return self.__data[key]

    def __setitem__(self, key: str, value: Union[str, int, float, bool]):
        self.__data[key] = value

    def __contains__(self, section: str):
        return section in self.__data

    def __len__(self):
        return len(self.__data)

    def __len__(self):
        return len(self.__data)
