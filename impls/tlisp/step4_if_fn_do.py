import sys
import traceback

from mal_types import Symbol, list_Q, symbol_Q
from printer import pr_str
from reader import read_str
from env import Env


def READ(val: str) -> str:
    return read_str(val)


def eval_ast(ast, env: Env):
    if symbol_Q(ast):
        if (fn := env.get(ast)):
            return fn
        raise Exception(f"'{ast}' not found")
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

    else:
        # apply
        fn, *args = eval_ast(ast, env)
        return fn(*args)


def PRINT(val: str) -> str:
    return pr_str(val)


repl_env = Env()
repl_env.set("+", lambda a, b: a + b)
repl_env.set("-", lambda a, b: a - b)
repl_env.set("*", lambda a, b: a * b)
repl_env.set("/", lambda a, b: int(a / b))


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val), repl_env))


while True:
    try:
        line = input("user> ")
        print(REP(line))
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
