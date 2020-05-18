from typing import Union


class Symbol(str):
    """symbol"""


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
