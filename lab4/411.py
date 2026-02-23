import json

def change(source, patch):
    for k, v in patch.items():
        if v is None:
            source.pop(k)
        elif k in source and isinstance(source[k], dict) and isinstance(v, dict):
            change(source[k], v)
        else:
            source[k] = v
    return source
    

source = json.loads(input()) 
patch = json.loads(input()) 

res = change(source, patch)
print(json.dumps(res, separators=(',', ':'), sort_keys=True))
