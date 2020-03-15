from sys import platform


def opsys():
    if platform == "darwin":
        return 0
    elif platform == "win32":
        return 1
    else:
        return -1
