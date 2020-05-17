def pr_str(val) -> str:
    """
    symbol: シンボルの文字列名を返す
    number: 数値を文字列で返す
    list: リストの各要素をループし、pr_str を呼び出す。その結果をスペースで結合、() で囲みかえす
    """

    if isinstance(val, str):
        return val
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, list):
        return "(" + " ".join(map(pr_str, val)) + ")"
    return val
