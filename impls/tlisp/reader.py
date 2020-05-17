"""
reader に関する処理
"""

import re
from typing import List, Optional, Union


class EndUnbalancedError(Exception):
    """カッコの対応ができていないときのエラー"""


tokens = [
    # 特殊な文字列 ~@
    r"~@",
    # 特殊な1文字 []{}()'`~^@
    r"[\[\]{}()'`~^@]",
    # " から始まって、" で終わる (末尾の " がない場合、エラーとして報告する必要がある)
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

    def peek(self) -> Union[str, None]:
        """
        現在の位置のトークンを返す
        チェックするためだけに使う (next() を読んでしまうと、位置を進めてしまうため)
        """
        return self.tokens[self.pos]

    def isEnd(self) -> bool:
        return self.pos >= len(self.tokens)


def read_str(val: str) -> str:
    """
    文字列からトークンのリストを生成し、Reader を生成し、データを返す
    """
    return read_form(Reader(tokenize(val)))


def tokenize(val: str) -> List[str]:
    """
    val 内に含まれるトークンのリストを返す
    """
    # 最後の空文字を削除
    return RE_TOKEN.findall(val)


# List[List[List[...]]] ってなるかもだから、どうしようか
def read_form(reader: Reader):
    """
    (1 2) => ["1", "2"]
    12 => "12"
    (+ 1 (* 2 3)) => ["+", "1", ["*", "2", "3"]]
    """
    if reader.isEnd():
        return None
    if reader.peek() == "(":
        return read_list(reader)
    return read_atom(reader)


# List[List[List[...]]] ってなるかもだから、どうしようか
def read_list(reader):
    result = []
    # ( の次のトークンに進める
    # ( + 1 2 )
    #   ^
    reader.next()

    peeked = ""
    while not (reader.isEnd() or reader.peek() == ")"):
        peeked = reader.peek()
        atom = read_form(reader)
        if atom is not None:
            result.append(atom)

    if reader.isEnd() and peeked != ")" or (not reader.isEnd() and reader.peek() != ")"):
        # 最後の文字が ) ではない
        raise EndUnbalancedError

    if not reader.isEnd() and reader.peek() == ")":
        # 次回、上のwhileに入れるようにするため
        # (+ (+ 1 2) (+ 2 3))
        #          ^ ^
        reader.next()

    return result


def read_atom(reader) -> str:
    atom = reader.next()

    # TODO: 文字列に対応する
    return atom
