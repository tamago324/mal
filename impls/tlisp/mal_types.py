class Symbol(str):
    """symbol"""


class MalFunc:
    """ fn* で定義された関数 """
    def __init__(self, ast, param, env, fn, is_macro=False):
        self.ast = ast
        self.param = param
        self.env = env
        self.fn = fn
        self.is_macro = is_macro


class Atom:
    def __init__(self, data) -> None:
        self.data = data

    def reset(self, data):
        self.data = data
        return data


class MalException(Exception):
    """ Exception """


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


def string_Q(val) -> bool:
    return type(val) == str


def atom_Q(val) -> bool:
    return isinstance(val, Atom)


def equals(a, b) -> bool:
    """ symbol と str を区別するため"""
    if symbol_Q(a) or symbol_Q(b):
        return (type(a) == type(b)) and a == b
    return a == b
