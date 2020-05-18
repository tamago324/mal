from printer import pr_str
from reader import read_str
import traceback
import sys


def READ(val: str) -> str:
    return read_str(val)


def EVAL(val: str) -> str:
    return val


def PRINT(val: str) -> str:
    return pr_str(val)


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val)))


while True:
    try:
        line = input("user> ")
        print(REP(line))
    except Exception:
        print(''.join(traceback.format_exception(*sys.exc_info())))
