from mal_types import list_Q, Atom, atom_Q, equals
from printer import pr_str, prn, println
import operator as op
from reader import read_str
from functools import reduce


def read_file(fname) -> str:
    with open(fname) as f:
        return "\n".join(f.readlines())


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
}
