from typing import Union


class Symbol(str):
    """symbol"""


class MalFunc:
    """ fn* で定義された関数 """
    def __init__(self, ast, param, env, fn):
        self.ast = ast
        self.param = param
        self.env = env
        self.fn = fn


def nil_Q(val) -> bool:
    return val is None


def true_Q(val) -> bool:
    return val is True


def false_Q(val) -> bool:
    return val is False


def symbol_Q(val) -> bool:
    return type(val) == Symbol


def list_Q(val) -> bool:
    return type(val) == list


def number_Q(val) -> bool:
    return type(val) == int


def function_Q(val) -> bool:
    return callable(val)


def malfunc_Q(val) -> bool:
    return isinstance(val, MalFunc)
