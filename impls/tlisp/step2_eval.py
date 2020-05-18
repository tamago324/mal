import sys
import traceback

from mal_types import list_Q, symbol_Q
from printer import pr_str
from reader import read_str

repl_env = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),
}


def READ(val: str) -> str:
    return read_str(val)


def eval_ast(ast, env):
    if symbol_Q(ast):
        if (fn := env.get(ast, None)):
            return fn
        raise Exception(f"'{ast}' is not found")
    elif list_Q(ast):
        return [EVAL(x, env) for x in ast]
    else:
        return ast


def EVAL(ast, env):
    if not list_Q(ast):
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast
    fn, *args = eval_ast(ast, env)
    return fn(*args)


def PRINT(val: str) -> str:
    return pr_str(val)


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val), repl_env))


while True:
    try:
        line = input("user> ")
        print(REP(line))
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
