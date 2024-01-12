# -*- coding: utf-8 -*-

import string
from common import *
from typing import Optional, Union


class Code:
    def __init__(
        self,
        *,
        title: str = '',
        authors: Union[str, list[str]] = '',
        comment: str = '',
        code: Union[str, bytes] = '',
        enabled: bool = False,
        raw_assembly: bool = False,
        assembly_ram_writes: Optional[bool] = None
    ):
        self.title = title
        self._authors = []
        self.authors = authors  # setter
        self._comment = comment  # setter
        self.code = code  # setter
        self.enabled = enabled
        self.raw_assembly = raw_assembly
        self.__assembly_ram_writes = assembly_ram_writes

    def __repr__(self):
        return '%s(title=\'%s\',author=\'%s\',comment=\'%s\',enabled=%s,assembly_ram_writes)' % (
            self.__class__.__name__, self.title, self.authors, self._comment, self.enabled)

    @property
    def arw_auto_detect(self):
        return self.__assembly_ram_writes is None

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code: Union[str, bytes]):
        if isinstance(code, bytes):
            code = code.hex()
        self.__code = self.format_code(code)

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, value: Union[str, list[str]]):
        if isinstance(value, str):
            self._authors = value
        elif isinstance(value, list):
            self._authors = ','.join(value)

    @property
    def comment(self):
        return self._comment.rstrip()

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    def __iadd__(self, other):
        if isinstance(other, bytes):
            other = other.hex()
        self.__code += other
        self.__code = self.format_code(self.__code)
        return self

    @property
    def assembly_ram_writes(self):
        if self.__assembly_ram_writes is not None:
            return self.__assembly_ram_writes

        # TODO 不完全
        for line in self.__code.splitlines():
            line = line.lstrip('#')
            if (
                line == 'D0000000 DEADCAFE' or
                line.startswith('C0') or
                line.startswith('00020000') or
                line.startswith('09020000')
            ):
                return False
        return True

    @assembly_ram_writes.setter
    def assembly_ram_writes(self, state: Union[bool, None]):
        self.__assembly_ram_writes = state

    # TODO コードが正しいか否かの関数 作らないなら削除
    # @classmethod
    # def check_code(cls, code: str):
    #     if len(cls.remove_white_space(code)) % 16 != 0:
    #         ...

    @classmethod
    def format_code(cls, code: str):
        code = cls.remove_white_space(code)

        result = ''

        i, c = 0, 0
        while i * 16 + c < len(code):
            p1 = code[i * 16 + c: i * 16 + 16 + c]
            p2 = code[i * 16 + c: i * 17 + 17]

            if p1.startswith('#'):
                c += 1
                line = p2[:9] + ' ' + p2[9:]
            else:
                line = p1[:8] + ' ' + p1[8:]

            result += line[:18] + '\n'

            i += 1

        return result.rstrip('\n').upper()

    @classmethod
    def remove_white_space(cls, string_: Union[str, None]):
        if string_ is None:
            return None
        for white_space in string.whitespace:
            string_ = string_.replace(white_space, '')
        return string_


class Codes:
    def __init__(self, *codes: Code):
        self.__codes: list[Code] = []
        self.add_code(*codes)

    def add_code(self, *codes: Code):
        for code in codes:
            self.__codes.append(code)

    def get_codes(self, enabled: Optional[bool] = None):
        return [code for code in self.__codes if enabled is None or (code.enabled == enabled)]

    def __delitem__(self, key: int):
        self.__codes.__delitem__(key)

    def __getitem__(self, key: int):
        return self.__codes[key]

    def __setitem__(self, key: int, value: Code):
        self.__codes[key] = value

    def __len__(self):
        return len(self.get_codes())
