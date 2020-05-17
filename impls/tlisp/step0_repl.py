def READ(val: str) -> str:
    return val


def EVAL(val: str) -> str:
    return val


def PRINT(val: str) -> str:
    return val


def REP(val: str) -> str:
    return PRINT(EVAL(READ(val)))


while True:
    line = input("user> ")
    print(REP(line))
