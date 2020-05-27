"""
reader に関する処理
"""

import re
from typing import List, Union

from mal_types import Symbol

tokens = [
    # 特殊な文字列 ~@
    r"~@",
    # 特殊な1文字 []{}()'`~^@
    r"[\[\]{}()'`~^@]",
    # " から始まって、" で終わる (末尾の " がない場合、エラーとして報告する必要がある)
    # string
    r'"(?:\\.|[^\\"])*"?',
    # ; で始まる文字列
    r";.*",
    # 0 文字以上の非特殊文字
    r"""[^\s\[\]{}('"`,;)]*""",
]

# トークンの正規表現
token_patterns = [
    # 無視される文字列 (空白、カンマ)
    r"[\s,]*",
    # キャプチャ
    r"(",
    "|".join(tokens),
    r")",
]

RE_TOKEN = re.compile("".join(token_patterns))


class Reader:
    def __init__(self, tokens: List[str]) -> None:
        self.tokens: List[str] = tokens
        self.pos = 0

    def next(self) -> str:
        """
        現在位置のトークンを返し、現在位置を進める
        """
        result = self.tokens[self.pos]
        self.pos += 1
        return result

    def peek(self):
        """
        現在の位置のトークンを返す
        チェックするためだけに使う (next() を読んでしまうと、位置を進めてしまうため)
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None


def read_str(val: str):
    """
    文字列からトークンのリストを生成し、Reader を生成し、データを返す
    """
    return read_form(Reader(tokenize(val)))


def tokenize(val: str):
    """
    val 内に含まれるトークンのリストを返す
    """
    # 最後の空文字を削除
    return RE_TOKEN.findall(val)


def read_form(reader: Reader):
    token = reader.peek()
    if token == "(":
        reader.next()
        return read_list(reader)

    elif re.match(r"^;.*", token):
        # comment
        return None

    # Reader macro
    elif token == "'":
        reader.next()
        return ["quote", read_form(reader)]
    elif token == "`":
        reader.next()
        return ["quasiquote", read_form(reader)]
    elif token == "~":
        reader.next()
        return ["unquote", read_form(reader)]
    elif token == "~@":
        reader.next()
        return ["splice-unquote", read_form(reader)]

    return read_atom(reader)


def read_list(reader):
    result = []
    # ( の次のトークンに進める
    # ( + 1 2 )
    #   ^
    peeked = ""
    while not (reader.peek() is None or reader.peek() == ")"):
        peeked = reader.peek()
        atom = read_form(reader)
        result.append(atom)

    if (
        reader.peek() is None
        and peeked != ")"
        or (reader.peek() is not None and reader.peek() != ")")
    ):
        # 最後の文字が ) ではない
        raise Exception("")

    if reader.peek() is not None and reader.peek() == ")":
        # 次回、上のwhileに入れるようにするため
        # (+ (+ 1 2) (+ 2 3))
        #          ^ ^
        reader.next()

    return result


def read_atom(reader):
    token = reader.next()

    if (match := re.match(r"^-?\d+$", token)):
        # Number
        return int(match.group())

    elif token == "nil":
        return None

    elif token == "true":
        return True

    elif token == "false":
        return False

    elif (match := re.match(r'"(?:\\.|[^\\"])*"?', token)):
        # TODO: 末尾の " がない場合、エラーにする
        # string
        s = match.group()[1:-1]
        # \n => 改行
        # \" => "
        # \\ => \
        # 順番大事
        return s.replace("\\\\", "\\").replace('\\"', '"').replace("\\n", "\n")

    # Symbol
    return Symbol(token)
