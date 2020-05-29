import operator as op
from functools import reduce

from mal_types import (
    Atom,
    MalException,
    atom_Q,
    equals,
    false_Q,
    list_Q,
    malfunc_Q,
    nil_Q,
    symbol_Q,
    true_Q,
)
from printer import pr_str, println, prn
from reader import read_str


def read_file(fname) -> str:
    with open(fname) as f:
        return "\n".join(f.readlines())


def throw(message):
    raise MalException(message)


def apply(fn, *args):
    args1 = list(args[:-1])
    args2 = args[-1]
    if malfunc_Q(fn):
        fn = fn.fn
    # * で list を展開する
    return fn(*(args1 + args2))


def map_(fn, list_):
    if malfunc_Q(fn):
        fn = fn.fn
    return list(map(fn, list_))


def nth(list_, n):
    try:
        return list_[n-1]
    except IndexError as e:
        raise MalException(e.args[0])


ns = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
    "%": op.mod,

    # 各引数を要素にしたリストを返す
    "list": lambda *args: list(args),

    # 第１引数がリストか
    "list?": list_Q,

    # リストが空か
    # nil はからのリストとする
    "empty?": lambda lst: True if lst is None else len(lst) == 0,

    # 要素数
    # nil は空のリスト
    "count": lambda lst: 0 if lst is None else len(lst),
    "nth": nth,

    "cons": lambda x, lst: [x] + lst,
    "concat": lambda *lists: reduce(op.add, lists) if len(lists) > 0 else [],

    "car": lambda lst: lst[0],
    "cdr": lambda lst: lst[1:],

    # 比較演算子
    "=": equals,
    "<": op.lt,
    "<=": op.le,
    ">": op.gt,
    ">=": op.ge,

    # 文字列を返す
    "pr-str": lambda *args: " ".join([pr_str(x, True) for x in args]),
    "str": lambda *args: "".join([pr_str(x, False) for x in args]),

    # 文字列を表示する
    "prn": prn,
    "println": println,

    "read-string": read_str,

    # デフォルトが r だから
    "slurp": read_file,

    # atom
    "atom": Atom,
    "atom?": atom_Q,
    # 値を返す
    "deref": lambda atom: atom.data,
    # 値の変更
    "reset!": lambda atom, val: atom.reset(val),

    "throw": throw,

    "apply": apply,
    "map": map_,

    "nil?": lambda x: nil_Q(x),
    "true?": lambda x: true_Q(x),
    "false?": lambda x: false_Q(x),
    "symbol?": lambda x: symbol_Q(x),
}
