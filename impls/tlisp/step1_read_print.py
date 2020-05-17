from printer import pr_str
from reader import read_str


def READ(val: str) -> str:
    return read_str(val)


def EVAL(val: str) -> str:
    return val


def PRINT(val: str) -> str:
    return pr_str(val)


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val)))


while True:
    line = input("user> ")
    print(REP(line))
