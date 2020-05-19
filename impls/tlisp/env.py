from __future__ import annotations

from typing import Any, Dict

from mal_types import Symbol


class Env:
    def __init__(self, outer_env: Env = None):
        self.env: Dict[Symbol, Any] = dict()
        self.outer_env = outer_env

    def set(self, k: Symbol, v) -> None:
        self.env[k] = v
        return v

    def get(self, k: Symbol):
        if (val := self.find(k)):
            return val
        raise Exception(f"'{k}' not found")

    def find(self, k: Symbol):
        """
        現在の環境に key があれば、それを返す
        なければ outer_env から探し、返す
        """
        if (val := self.env.get(k)):
            return val
        if self.outer_env is not None:
            return self.outer_env.find(k)
        return None
