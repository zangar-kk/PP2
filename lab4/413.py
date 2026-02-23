import json

def resolve(data, query):
    cur = data
    i = 0
    n = len(query)

    try:
        while i < n:
            ch = query[i]

            if ch == '.':
                i += 1
                continue

            if ch == '[':
                i += 1
                if i >= n:
                    return None

                if not query[i].isdigit():
                    return None
                idx = 0
                while i < n and query[i].isdigit():
                    idx = idx * 10 + (ord(query[i]) - ord('0'))
                    i += 1

                if i >= n or query[i] != ']':
                    return None
                i += 1

                if not isinstance(cur, list):
                    return None
                cur = cur[idx]
                continue

            if ch.isalpha() or ch == '_':
                start = i
                i += 1
                while i < n and (query[i].isalnum() or query[i] == '_'):
                    i += 1
                key = query[start:i]

                if not isinstance(cur, dict) or key not in cur:
                    return None
                cur = cur[key]
                continue

            return None

        return cur

    except (KeyError, IndexError, TypeError):
        return None


data = json.loads(input())
q = int(input())

for _ in range(q):
    query = input().strip()
    ans = resolve(data, query)
    if ans is None:
        print("NOT_FOUND")
    else:
        print(json.dumps(ans, separators=(",", ":"), sort_keys=True))