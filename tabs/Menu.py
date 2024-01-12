# -*- coding: utf-8 -*-

class Menu:
    def __init__(
        self,
        *,
        keys: str,
        title: str,
        description: str,
    ):
        self.keys = keys
        self.title = title
        self.description = description

    def run(self, **kwargs):
        raise Exception('Class \'%s\' has no run()' % (self.__class__.__name__))
