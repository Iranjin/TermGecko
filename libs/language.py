# -*- coding: utf-8 -*-

import os
from typing import Optional


class Language:
    def __init__(self):
        self.__path = None
        self.__encoding = None
        self.__data = None

    def __detect_encoding(self, path: str):
        # TODO 種類が少ない
        encodings = [
            'cp932',
            'ascii',
            'utf-8',
            'utf-16',
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

    # def __section_error(self, section_name: str):
    #     raise KeyError('Invalid or missing %s section in the language file.' % (section_name))

    @property
    def loaded(self):
        return self.__data is not None

    def load(self, path: str, encoding: Optional[str] = None):
        if not os.path.exists(path):
            raise FileNotFoundError('File \'%s\' not found' % (path))

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

            # Comment
            if line.startswith((';', '#')):
                pass

            # Set section
            elif line.startswith('[') and line.endswith(']'):
                current_section = line.lstrip('[').rstrip(']')

            # Keys
            elif '=' in line:
                if current_section is None:
                    raise SyntaxError('Section is not set')

                item = line.split('=')

                key = item[0]
                value = item[1]

                if value.startswith(('"', '\'')) and value.endswith(('"', '\'')):
                    # translate_table = str.maketrans({'\\n': '\n', '\\t': '\t'})
                    # value = value.strip('" \'').translate(translate_table)
                    value = value.strip('" \'')
                else:
                    # 文字列がダブルクォーテーションまたはクォーテーションで囲まれていなかった場合
                    raise SyntaxError(
                        'String must be enclosed in double quotation marks or quotation marks')

                result.setdefault(current_section, {})
                result[current_section][key] = value

        self.__data = result

    def __getitem__(self, key: str):
        table = self.__data['TABLE']
        value = table.get(key)
        return 'Null' if value is None else value

    def get_info(self):
        return self.__data['INFORMATION']
