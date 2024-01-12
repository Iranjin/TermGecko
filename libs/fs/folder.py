# -*- coding: utf-8 -*-

from .imports import *
from .file import File


class Folder:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def __str__(self) -> str:
        return self.path

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def is_dir(self) -> bool:
        return os.path.isdir(self.path)

    def create(self) -> 'Folder':
        os.makedirs(self.path)
        return self

    def remove(self) -> 'Folder':
        for root, dirs, files in os.walk(self.path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.path)
        return self

    def glob(self, pattern: str, return_path: bool = False) -> list[Union[str, File]]:
        pattern_ = re.compile(pattern)

        matches: list[Union[str, File]] = []
        for root, _, files in os.walk(self.path):  # NOTE _はディレクトリ
            for file in files:
                if pattern_.match(file):
                    path = os.path.join(root, file)
                    matches.append(path if return_path else File(path))

        return matches
