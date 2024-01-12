# -*- coding: utf-8 -*-

from typing import (
    Callable,
    Optional,
    Union,
    Any,
)


class Command:
    class Arg:
        def __init__(self, name: str, type_: type) -> None:
            self.__name = name
            self.__type: type = type_
            self.__key: Callable[[Any], bool] = None

        def get_type(self) -> type:
            return self.__type

        def get_name(self) -> type:
            return self.__name

        def set_arg(self, key: Callable[[Any], bool] = None) -> None:
            self.__key = key

        def __parse(self, arg: Callable[[Any], bool]) -> bool:
            if self.__key is None:
                return True
            else:
                return self.__key(arg)

        def parse(self, data: Optional[Any] = None) -> bool:
            if not isinstance(data, self.__type):
                raise TypeError('Unsupported operand type for parse(): \'%s\'' % (
                    self.__type.__name__))
            elif isinstance(data, (str, int)):
                return self.__parse(data)
            elif data is None:
                return None

    # Struct

    class Result:
        def __init__(
            self,
            valid: Optional[bool] = None,
            arg: Optional[Any] = None
        ) -> None:
            self.valid: Optional[bool] = valid
            self.arg: Optional[Any] = arg

    def __init__(self, **kwargs: Union[type, tuple[type, Callable[[Any], bool]]]) -> None:
        self.__args: list[Command.Arg] = []

        for arg in kwargs.items():
            name: str = arg[0]
            key: Callable[[Any], bool] = None

            if isinstance(arg[1], tuple):
                type_: type = arg[1][0]
                key = arg[1][1]
            else:
                type_: type = arg[1]

            arg_instance = Command.Arg(name, type_)
            arg_instance.set_arg(key)

            self.__args.append(arg_instance)

    def clear(self) -> None:
        self.__args.clear()

    def parse(self, args: str, split_char: str = ' ') -> dict[str, 'Command.Result']:
        splitted_args: list[str] = [char for char in args.split(split_char) if char != split_char]

        if len(splitted_args) < self.__len__():
            raise ValueError('Missing %d required positional argument' % (
                self.__len__() - len(splitted_args)))
        elif len(splitted_args) > self.__len__():
            raise ValueError('Takes %d positional arguments but %d were given' % (
                self.__len__(), len(splitted_args)))

        result: dict[str, Command.Result] = {}

        for text, arg in zip(splitted_args, self.__args):
            valid: bool = False
            arg_: Any = None

            try:
                valid = arg.parse(arg.get_type()(text))
            except:
                valid = False

            try:
                arg_ = arg.get_type()(text)
            except:
                pass

            result[arg.get_name()] = Command.Result(valid, arg_)

        return result

    def input(self, __prompt: object = '', _exit: bool = False) -> dict[str, 'Command.Result']:
        text = input(__prompt)
        if _exit and text == '':
            return None
        return self.parse(text)

    def __len__(self) -> int:
        return len(self.__args)
