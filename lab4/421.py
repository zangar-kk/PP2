import importlib

n = int(input())

for i in range(n):
    mod, func = input().split()

    try:
        module = importlib.import_module(mod)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, func):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    attr = getattr(module, func)

    if callable(attr):
        print("CALLABLE")
    else:
        print("VALUE")