# -*- coding: utf-8 -*-

from .Menu import Menu
from libs.config import Config
from libs.language import Language
from common import *


class TemplateMenu(Menu):
    def __init__(self, config: Config, language: Language):
        super().__init__(
            title='Template',  # 名前
            description='template menu',  # 説明文
            keys=('t')  # メニューを開くコマンド(複数のエイリアスを設定可能)
        )
        self.__config = config
        self.__language = language

    def run(self, **kwargs):
        text = input('TemplateMenu > ')

        # コンフィグファイルからIPアドレスをロード
        ip_address = self.__config.get('TCPGecko', 'IPAddress')

        # 言語ファイルから文字列をロード
        string_ = self.__language['something_went_wrong']

        for _ in range(5):
            print(text + '!!')

        input()

        return 0  # 0を返すとループ終了
