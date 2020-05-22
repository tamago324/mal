from mal_types import list_Q
from printer import pr_str
import operator as op


ns = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
    "%": op.mod,

    # 各引数を要素にしたリストを返す
    "list": list,

    # 第１引数がリストか
    "list?": list_Q,

    # リストが空か
    # nil はからのリストとする
    "empty?": lambda lst: True if lst is None else len(lst) == 0,

    # 要素数
    # nil は空のリスト
    "count": lambda lst: 0 if lst is None else len(lst),

    # 比較演算子
    "=": op.eq,
    "<": op.lt,
    "<=": op.le,
    ">": op.gt,
    ">=": op.ge,

    # TODO:
    "prn": pr_str,
}
