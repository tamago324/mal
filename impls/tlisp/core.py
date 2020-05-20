from mal_types import list_Q
from printer import pr_str


ns = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),
    "%": lambda a, b: int(a % b),

    # 各引数を要素にしたリストを返す
    "list": lambda *args: list(args),

    # 第１引数がリストか
    "list?": lambda lst: list_Q(lst),

    # リストが空か
    # nil はからのリストとする
    "empty?": lambda lst: True if lst is None else len(lst) == 0,

    # 要素数
    # nil は空のリスト
    "count": lambda lst: 0 if lst is None else len(lst),

    # 比較演算子
    "=": lambda a, b: a == b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,

    # TODO:
    "prn": pr_str,
}
