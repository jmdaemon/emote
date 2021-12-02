import json

def to_charmap(jstr: str) -> dict:
    '''Converts a json string to a charmap dictionary'''
    data = json.loads(jstr)
    return data

def read_file(fname: str) -> str:
    file = open(fname, 'r')
    res = file.read()
    file.close()
    return res

def read_charmap(conts: str) -> dict:
    return(to_charmap(read_file(conts)))

# Convert character maps to json
def to_json(charmap: dict) -> str:
    ''' Converts a dictionary charmap to json '''
    o = json.dumps(charmap, indent=4, ensure_ascii=False) # Don't unescape Unicode characters
    return o

def export_charmap(fname: str, charmap: dict):
    file = open(fname, 'w')
    output = to_json(charmap)
    file.write(output)
    file.close()
