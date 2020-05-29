import sys
import traceback

import core
from env import Env
from mal_types import MalFunc, Symbol, list_Q, malfunc_Q, symbol_Q
from printer import pr_str
from reader import read_str


def is_pair(ast) -> bool:
    """ 空ではないリストなら、True """
    return True if list_Q(ast) and len(ast) > 0 else False


def quasiquote(ast):
    if not is_pair(ast):
        # quote と同じように処理する
        return [Symbol("quote"), ast]
    elif ast[0] == "unquote":
        return ast[1]
    elif is_pair(ast[0]) and ast[0][0] == "splice-unquote":
        # ast が ((splice-unquote lst) 1 2 3) の場合
        # ast[0]    => (splice-unquote lst)
        # ast[0][1] => lst
        # ast[1:]   => (1 2 3)
        return [Symbol("concat"), ast[0][1], quasiquote(ast[1:])]
    else:
        return [Symbol("cons"), quasiquote(ast[0]), quasiquote(ast[1:])]


def is_macro_call(ast, env) -> bool:
    return (
        list_Q(ast)
        and symbol_Q(ast[0])
        and malfunc_Q(env.get(ast[0]))
        and env.get(ast[0]).is_macro
    )


def macroexpand(ast, env):
    while is_macro_call(ast, env):
        macro = env.get(ast[0])
        # 展開してあげないといけない
        ast = macro.fn(*ast[1:])
    return ast


def READ(val: str) -> str:
    return read_str(val)


def eval_ast(ast, env: Env):
    if symbol_Q(ast):
        # env から取得した値を返す
        if (val := env.get(ast)) is None:
            raise Exception(f"'{ast}' not found")
        return val
    elif list_Q(ast):
        return [EVAL(x, env) for x in ast]
    else:
        return ast


def EVAL(ast, env: Env):
    while True:
        if not list_Q(ast):
            return eval_ast(ast, env)
        if len(ast) == 0:
            return ast

        # 評価するときにマクロを実行し、書き換える
        ast = macroexpand(ast, env)
        if not list_Q(ast):
            return eval_ast(ast, env)

        # special atom
        if ast[0] == "def!":
            # XXX: return いる？
            return env.set(ast[1], EVAL(ast[2], env))

        elif ast[0] == "let*":
            # 次のループに env と ast を渡す感じ
            # Tail call
            env = Env(env)
            for i in range(0, len(ast[1]), 2):
                symbol, val = ast[1][i], ast[1][i + 1]
                env.set(symbol, EVAL(val, env))
            ast = ast[2]

        elif ast[0] == "fn*":
            # (fn* (a b) (+ a b))
            # (a b) を仮引数とする (Symbol のリスト)
            # (+ a b) を EVAL() で評価する
            # 関数実行時に渡される実引数のリストと Symbol のリストとして、環境を作る
            return MalFunc(
                ast=ast[2],
                param=ast[1],
                env=env,
                fn=lambda *args: EVAL(ast[2], Env(env, ast[1], *args)),
            )

        elif ast[0] == "if":
            res = EVAL(ast[1], env)
            if not (res is None or res is False):
                # 0 は True とする
                ast = ast[2]
            else:
                if len(ast) < 4:
                    # false だったときの値がなければ、nil を返す
                    ast = None
                ast = ast[3]

        elif ast[0] == "do":
            eval_ast(ast[1:-1], env)
            # 最後の評価は後で評価する
            # 末尾呼び出しのため
            ast = ast[-1]

        elif ast[0] == "quote":
            # データですよーって伝えられた ==> 評価せずに返す
            return ast[1]

        elif ast[0] == "quasiquote":
            ast = quasiquote(ast[1])

        elif ast[0] == "defmacro!":
            # (defmacro! one (fn* () 1))
            #                     ^^ ^
            fn = ast[2]
            macro = MalFunc(
                ast=fn[2],
                param=fn[1],
                env=env,
                fn=lambda *args: EVAL(fn[2], Env(env, fn[1], *args)),
                is_macro=True,
            )
            return env.set(ast[1], EVAL(macro, env))

        elif ast[0] == "macroexpand":
            return macroexpand(ast[1], env)

        elif ast[0] == "try*":
            # e,g,: (try* abc (catch* e (prn "e is: " e)))
            try:
                # ここで呼び出すのは、try の中で実行するため
                return EVAL(ast[1], env)
            except Exception as e:
                # 新しい env を作り、評価
                message = e.args[0]
                env = Env(env, [ast[2][1]], message)
                return EVAL(ast[2][2], env)

        else:
            # apply
            fn, *args = eval_ast(ast, env)
            if isinstance(fn, MalFunc):
                ast = fn.ast
                env = Env(fn.env, fn.param, *args)
            else:
                return fn(*args)


def PRINT(val: str) -> str:
    return pr_str(val)


repl_env = Env()
for symbol, func in core.ns.items():
    repl_env.set(symbol, func)
repl_env.set("eval", lambda ast: EVAL(ast, repl_env))

# fn を適用してセット
repl_env.set(
    "swap!", lambda atom, fn, *args: atom.reset(EVAL([fn, atom.data, *args], repl_env))
)


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val), repl_env))


REP('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))')
REP("(def! inc (fn* (x) (+ x 1)))")
REP("(def! dec (fn* (x) (- x 1)))")
REP("(def! not (fn* (expr) (if expr false true)))")


while True:
    try:
        line = input("user> ")
        if line is None:
            continue
        print(REP(line))
    except Exception:
        print("".join(traceback.format_exception(*sys.exc_info())))
