import json
import wora.file

cmapdefs = {
    'bold': 'bold.json',
    'boldSans': 'bold-sans.json',
    'boldItalic': 'bold-italic.json', # Note: The h character is missing
    'boldItalicSans': 'bold-italic-sans.json',
    'italic': 'italic.json',
    'italicSans': 'italic-sans.json',
    'subscript': 'subscripts.json',
    'superscript': 'superscripts.json',
    'doubleStruck': 'doublestruck.json',
    'oldEnglish': 'old-eng.json',
    'medieval': 'med.json',
    'monospace': 'monospace.json',
}

def to_charmap(jstr: str) -> dict:
    '''Converts a json string to a charmap dictionary'''
    data = json.loads(jstr)
    return data

# Convert character maps to json
def to_json(charmap: dict) -> str:
    ''' Converts a dictionary charmap to json '''
    o = json.dumps(charmap, indent=4, ensure_ascii=False) # Don't unescape Unicode characters
    return o

def export_charmap(charmap: dict, fname: str):
    wora.file.write_file(fname, to_json(charmap))
