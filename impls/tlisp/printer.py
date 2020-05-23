from mal_types import (
    Symbol,
    false_Q,
    function_Q,
    list_Q,
    malfunc_Q,
    nil_Q,
    number_Q,
    string_Q,
    symbol_Q,
    true_Q,
    atom_Q,
)


def pr_str(val, print_readably: bool = True) -> str:
    """
    symbol: シンボルの文字列名を返す
    number: 数値を文字列で返す
    list: リストの各要素をループし、pr_str を呼び出す。その結果をスペースで結合、() で囲みかえす

    print_readably
        true の場合、read_atom() を適用する前の文字列に変換する
    """

    if symbol_Q(val):
        return val
    elif list_Q(val):
        return "(" + " ".join(map(pr_str, val)) + ")"
    elif nil_Q(val):
        return "nil"
    elif true_Q(val):
        return "true"
    elif false_Q(val):
        return "false"
    elif number_Q(val):
        return str(val)
    elif function_Q(val):
        return "#<function>"
    elif malfunc_Q(val):
        return "#<function>"
    elif atom_Q(val):
        return f"(atom {val.data})"
    if print_readably:
        # 改行 => \n
        # "    => \"
        # \    => \\
        val = '"' + val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
    return val


def prn(*args):
    print(" ".join([pr_str(x, True) for x in args]))
    # nil
    return None


def println(*args):
    print(" ".join([pr_str(x, False) for x in args]))
    # nil
    return None
