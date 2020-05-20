from __future__ import annotations

from typing import Any, Dict

from mal_types import Symbol


class Env:
    def __init__(self, outer_env: Env = None, binds=[], *exprs):
        """
        binds:
            Symbol のリスト (仮引数のリスト)
        exprs:
            値のリスト (実引数のリスト)
        """
        self.env: Dict[Symbol, Any] = dict()
        self.outer_env = outer_env

        # 関数の引数の環境を追加
        for i, symbol in enumerate(binds):
            self.env[symbol] = exprs[i]

    def set(self, k: Symbol, v) -> None:
        self.env[k] = v
        return v

    def get(self, k: Symbol):
        if (val := self.find(k)) is not None:
            # 0 も False になってしまうため
            return val
        return None

    def find(self, k: Symbol):
        """
        現在の環境に key があれば、それを返す
        なければ outer_env から探し、返す
        """
        if (val := self.env.get(k)) is not None:
            return val
        if self.outer_env is not None:
            return self.outer_env.find(k)
        return None
