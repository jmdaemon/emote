import json

def to_charmap(o: str) -> dict:
    ''' Converts a json string to a charmap dictionary '''
    # data = json.load(o)
    data = json.loads(o)
    # print(data)
    return data

# Convert character maps to json
def to_json(charmap: dict) -> str:
    ''' Converts a dictionary charmap to json '''
    o = json.dumps(charmap, indent=4, ensure_ascii=False) # Don't unescape Unicode characters
    return o

def read_file(fname: str) -> str:
    file = open(fname, 'r')
    res = file.read()
    file.seek(0)
    file.close()
    return res

def read_charmap(conts: str) -> dict:
    return(to_charmap(conts))

def export_charmap(fname: str, charmap: dict):
    file = open(fname, 'w')
    output = to_json(charmap)
    file.write(output)
    file.close()
