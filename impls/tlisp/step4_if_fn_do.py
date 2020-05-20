import sys
import traceback

from mal_types import Symbol, list_Q, symbol_Q
from printer import pr_str
from reader import read_str
from env import Env
import core


def READ(val: str) -> str:
    return read_str(val)


def eval_ast(ast, env: Env):
    if symbol_Q(ast):
        if (symbol := env.get(ast)) is None:
            raise Exception(f"'{ast}' not found")
        return symbol
    elif list_Q(ast):
        return [EVAL(x, env) for x in ast]
    else:
        return ast


def EVAL(ast, env: Env):
    if not list_Q(ast):
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast

    # special atom
    if ast[0] == 'def!':
        # XXX: return いる？
        return env.set(ast[1], EVAL(ast[2], env))

    elif ast[0] == 'let*':
        new_env = Env(env)
        env_pair = ast[1]
        for i in range(int(len(env_pair) / 2)):
            k, v = env_pair[i*2], env_pair[i*2+1]
            new_env.set(k, EVAL(v, new_env))
        return EVAL(ast[2], new_env)

    elif ast[0] == 'fn*':
        # (fn* (a b) (+ a b))
        # (a b) を仮引数とする (Symbol のリスト)
        # (+ a b) を EVAL() で評価する
        # 関数実行時に渡される実引数のリストと Symbol のリストとして、環境を作る
        return lambda *args: EVAL(ast[2], Env(env, ast[1], *args))

    elif ast[0] == 'if':
        res = EVAL(ast[1], env)
        if not(res is None or res is False):
            # 0 は True とする
            return EVAL(ast[2], env)
        else:
            if len(ast) < 4:
                # false だったときの値がなければ、nil を返す
                return None
            return EVAL(ast[3], env)

    elif ast[0] == 'do':
        # すべての引数を EVAL で評価して、最後の引数の評価結果を返す
        # `(do (def! a 1) (def! a (+ a 20)))`
        # => 21
        return [EVAL(x, env) for x in ast[1:]][-1]

    else:
        # apply
        fn, *args = eval_ast(ast, env)
        return fn(*args)


def PRINT(val: str) -> str:
    return pr_str(val)


repl_env = Env()
for symbol, func in core.ns.items():
    repl_env.set(symbol, func)


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val), repl_env))


while True:
    try:
        line = input("user> ")
        print(REP(line))
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
