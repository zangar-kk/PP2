import json

def lit(v):
    return json.dumps(v, separators=(",", ":"), sort_keys=True)

def diff(a, b, path=""):
    res = []

    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for k in keys:
            new_path = f"{path}.{k}" if path else k

            if k not in a:
                res.append((new_path, "<missing>", b[k]))
            elif k not in b:
                res.append((new_path, a[k], "<missing>"))
            else:
                res.extend(diff(a[k], b[k], new_path))
        return res

    if a != b:
        res.append((path, a, b))

    return res


obj1 = json.loads(input())
obj2 = json.loads(input())

ans = diff(obj1, obj2)

if not ans:
    print("No differences")
else:
    ans.sort(key=lambda x: x[0])
    for p, old, new in ans:
        old_val = old if old == "<missing>" else lit(old)
        new_val = new if new == "<missing>" else lit(new)
        print(f"{p} : {old_val} -> {new_val}")