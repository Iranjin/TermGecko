# -*- coding: utf-8 -*-

from .codes import Code, Codes
from typing import Optional
import xml.etree.ElementTree as ET
import xml.dom.minidom


class CodeParser:
    NONE_STR = '*/None/*'

    def __init__(self):
        self.__codes = Codes()
        self.__path: str = None
        self.__encoding: str = None
        self.__xml_mode: str = None

    def __detect_encoding(self, path: str):
        # TODO 種類が少ない
        encodings = [
            'utf-8',
            'utf-16',
            'cp932',
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

    def __parse_xml(self, path: str, encoding: Optional[str] = None):
        if encoding is None:
            encoding = self.__detect_encoding(path)

        with open(path, 'r', encoding=encoding) as f:
            xml_data = f.read()
        self.__path = path
        self.__encoding = encoding

        self.__codes = Codes()

        root = ET.fromstring(xml_data)

        entries = root.findall('./entry')

        def set_attribute(entry: ET.Element, attribute: str, instance, attribute_name: str, convert_to_bool: bool = False):
            attribute_value = entry.find(attribute).text
            if attribute_value is not None:
                if convert_to_bool:
                    setattr(instance, attribute_name, attribute_value.lower() == 'true')
                else:
                    setattr(instance, attribute_name, attribute_value)

        for entry in entries:
            code_instance = Code()

            code_instance.title = entry.get('name')
            set_attribute(entry, './code', code_instance, 'code')
            set_attribute(entry, './authors', code_instance, 'authors')
            # set_attribute(entry, './raw_assembly', code_instance, 'raw_assembly', convert_to_bool=True)
            set_attribute(entry, './raw_assembly', code_instance, 'raw_assembly', convert_to_bool=True)
            set_attribute(entry, './assembly_ram_write', code_instance, 'assembly_ram_writes', convert_to_bool=True)
            set_attribute(entry, './comment', code_instance, 'comment')
            set_attribute(entry, './enabled', code_instance, 'enabled', convert_to_bool=True)

            self.__codes.add_code(code_instance)

    # NOTE '\n\n'で分割してから解析
    def __parse_codelist(self, path: str, encoding: Optional[str] = None):
        if encoding is None:
            encoding = self.__detect_encoding(path)

        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        self.__path = path

        entries = content.split('\n\n')

        self.__codes = Codes()

        for entry in entries:
            lines = entry.splitlines()

            code_instance = Code()
            code_instance.assembly_ram_writes
            count = 0
            while lines:
                line = lines.pop(0)

                if line != '':
                    # authors
                    if line.startswith('@'):
                        code_instance.authors = line.lstrip('@ ')
                        count -= 1
                    # comment
                    elif line.startswith('//'):
                        code_instance._comment += line.lstrip('// ') + '\n'
                        count -= 1
                    elif count == 0:
                        code_instance.title = '' if line == self.NONE_STR else line
                    elif count == 1:
                        flags = line.split()
                        code_instance.enabled = flags[0].lower() == 'on'
                        if len(flags) >= 2:
                            code_instance.assembly_ram_writes = flags[1].lower() == 'on'
                    elif count >= 2:
                        if line == self.NONE_STR:
                            code_instance.code = ''
                        else:
                            code_instance.code += line
                    count += 1

                if not lines or line == '':
                    self.__codes.add_code(code_instance)
                    code_instance = Code()
                    count = 0

    # NOTE 一行ずつ解析バージョン
    # def __parse_codelist(self, path: str, encoding: Optional[str] = None):
    #     if encoding is None:
    #         encoding = self.__detect_encoding(path)

    #     with open(path, 'r', encoding=encoding) as f:
    #         content = f.read()
    #     self.__path = path
    #     self.__encoding = encoding

    #     lines = content.splitlines()

    #     self.__codes = Codes()
    #     code_instance = Code()
    #     code_instance.assembly_ram_writes
    #     count = 0
    #     while lines:
    #         line = lines.pop(0)

    #         if line != '':
    #             # authors
    #             if line.startswith('@'):
    #                 code_instance.authors = line.lstrip('@ ')
    #                 count -= 1
    #             # comment
    #             elif line.startswith('//'):
    #                 code_instance._comment += line.lstrip('// ') + '\n'
    #                 count -= 1
    #             elif count == 0:
    #                 code_instance.title = '' if line == self.NONE_STR else line
    #             elif count == 1:
    #                 flags = line.split()
    #                 code_instance.enabled = flags[0].lower() == 'on'
    #                 if len(flags) >= 2:
    #                     code_instance.assembly_ram_writes = flags[1].lower() == 'on'
    #             elif count >= 2:
    #                 if line == self.NONE_STR:
    #                     code_instance.code = ''
    #                 else:
    #                     code_instance.code += line
    #             count += 1

    #         if not lines or line == '':
    #             self.__codes.add_code(code_instance)
    #             code_instance = Code()
    #             count = 0

    def __save_xml(self, indent: Optional[int] = None):
        if indent is None:
            indent = 4

        root = ET.Element('codes')

        for code_instance in self.__codes:
            entry = ET.Element('entry', attrib={'name': code_instance.title})

            code_element = ET.Element('code')
            code_element.text = code_instance.code
            entry.append(code_element)

            authors_element = ET.Element('authors')
            authors_element.text = code_instance.authors
            entry.append(authors_element)

            raw_assembly_element = ET.Element('raw_assembly')
            raw_assembly_element.text = 'true' if code_instance.raw_assembly else 'false'
            entry.append(raw_assembly_element)

            assembly_ram_write_element = ET.Element('assembly_ram_write')
            assembly_ram_write_element.text = 'true' if code_instance.assembly_ram_writes else 'false'
            entry.append(assembly_ram_write_element)

            comment_element = ET.Element('comment')
            comment_element.text = code_instance.comment
            entry.append(comment_element)

            enabled_element = ET.Element('enabled')
            enabled_element.text = 'true' if code_instance.enabled else 'false'
            entry.append(enabled_element)

            root.append(entry)

        dom = xml.dom.minidom.parseString(ET.tostring(root))

        with open(self.__path, 'wb') as f:
            f.write(dom.toprettyxml(' ' * indent, encoding='UTF-16'))

    def __save_codelist(self, indent: Optional[int] = None, format_code: bool = True):
        if indent is None:
            indent = 1

        lines: list[str] = []

        for code_instance in self.__codes:
            if code_instance.title != '':
                lines.append(code_instance.title)
            else:
                lines.append(self.NONE_STR)
            if code_instance.authors != '':
                lines.append('@ ' + code_instance.authors)
            if code_instance._comment != '':
                lines.append('\n'.join('// ' + line for line in code_instance._comment.splitlines()))
            lines_: list[str] = []
            lines_.append('on' if code_instance.enabled else 'off')
            if code_instance.assembly_ram_writes is not None:
                if not code_instance.arw_auto_detect:
                    lines_.append('on' if code_instance.assembly_ram_writes else 'off')
            lines.append(' '.join(lines_))
            if code_instance.code != '':
                lines.append(code_instance.code if format_code else Code.remove_white_space(code_instance.code))
            else:
                lines.append(self.NONE_STR)
            lines.append('\n' * (indent - 1))
        result = '\n'.join(lines).rstrip('\n')

        with open(self.__path, 'w', encoding=self.__encoding) as f:
            f.write(result)

    def load(self, path: str, encoding: Optional[str] = None):
        if path.lower().endswith('.xml'):
            self.__xml_mode = True
            self.__parse_xml(path, encoding)
        else:
            self.__xml_mode = False
            self.__parse_codelist(path, encoding)

    def save(self, indent: int = 1, format_code: bool = True):
        if self.__xml_mode:
            self.__save_xml(indent)
        else:
            self.__save_codelist(indent, format_code)

    @ property
    def codes(self):
        return self.__codes

    @ codes.setter
    def codes(self, value: Codes):
        self.__codes = value

    def __setitem__(self, key: int, code: Code):
        self.__codes[key] = code

    def __getitem__(self, key: int):
        data = self.__codes[key]
        return data

    def __delitem__(self, key: int):
        del self.__codes[key]

    def __len__(self):
        return len(self.__codes)
