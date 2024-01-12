# -*- coding: utf-8 -*-

from .imports import *


class File:
    def __init__(self, path: str = '', encoding: Optional[str] = None) -> None:
        self.path = path
        self.__enc = encoding

    def __str__(self) -> str:
        return self.path

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

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def is_file(self) -> bool:
        return os.path.isfile(self.path)

    @property
    def fp(self):
        return io.BytesIO(self.read(bytes))

    @property
    def encoding(self) -> str:
        return self.__enc

    @property
    def current_dir(self) -> str:
        return os.path.dirname(self.path)

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    def rename(self, name: str) -> 'File':
        os.rename(
            self.path,
            os.path.join(self.current_dir, name)
        )
        return self

    def create(self) -> 'File':
        with open(self.path, 'a') as f:
            pass
        return self

    def size(self) -> int:
        return os.path.getsize(self.path)

    def remove(self) -> 'File':
        os.remove(self.path)
        return self

    def write(self, data: Union[str, int, bytes], over_write: bool = True) -> 'File':
        mode: str = 'w' if over_write else 'a'

        if isinstance(data, (str, int)):
            with open(self.path, mode, encoding=self.__enc) as f:
                f.write(str(data))
        elif isinstance(data, bytes):
            mode += 'b'
            with open(self.path, mode) as f:
                f.write(data)
        else:
            raise TypeError('Unsupported operand type for write(): \'%s\'' % (
                type(data).__name__))

        return self

    def read(self, type_: Union[str, int, bytes] = str) -> Union[str, int, bytes]:
        if type_ == str or type_ == int:
            result: str = ''
            encoding = self.__enc
            if encoding is None:
                encoding = self.__detect_encoding(self.path)
            with open(self.path, 'r', encoding=self.__enc) as f:
                result = f.read()
            return type_(result)
        elif type_ == bytes:
            result: bytes = b''
            with open(self.path, 'rb') as f:
                result = f.read()
            return result
        else:
            raise TypeError('Unsupported operand type for read(): \'%s\'' % (
                type_.__name__))


def get_file(
    url: str,
    obj: type = bytes,
    encoding: Optional[str] = None,
    headers: Optional[dict[str, str]] = None
) -> Union[str, Any]:
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    ssl._create_default_https_context: ssl.SSLContext = ssl._create_unverified_context

    req = urllib.request.Request(url, headers=headers)
    response: bytes = urllib.request.urlopen(req).read()

    if obj == bytes:
        return response
    else:
        return obj(response.decode(encoding))
