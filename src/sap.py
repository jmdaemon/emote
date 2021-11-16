from cmapdefs import *
import sys
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def convert(char_map, text):
    out = ""
    for char in text:
        if char in char_map:
            out += char_map[char]
        elif char.lower() in char_map:
            out += char_map[char.lower()]
        else:
            out += char
    return out

def strikethrough(text, strikeover):
    return ''.join([char + strikeover for char in text])

def main():
    parser = argparse.ArgumentParser(description='Apply string manipulations on text')
    parser.add_argument('text', metavar='<text>', type=str)
    parser.add_argument('effects', help='Apply string manipulation', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    text = str(args.text) if str(args.text) else ''
    effects = args.effects

    if not text:
        sys.exit()

    out = ""
    if (len(effects) < 1):
        print("Usage")
    elif(len(effects) < 2):
        cmd = effects[0]
        if (cmd == 'v' or cmd == '--version'):
            MAJOR, MINOR, PATCH = '0', '1', '0'
            print(f'strmanip - v{MAJOR}.{MINOR}.{PATCH}')
            sys.exit()
        if (cmd == '--sub'):
            out = convert(subscriptCharMap, text)
        if (cmd == '--super'):
            out = convert(superscriptCharMap, text)
        if (cmd == '-ds' or cmd == '--doublestruck'):
            out = convert(doubleStruckCharMap, text)
        if (cmd == '-oe' or cmd == '--oldeng'):
            out = convert(oldEnglishCharMap, text)
        if (cmd == '-med' or cmd == '--medieval'):
            out = convert(medievalCharMap, text)
        if (cmd == '-mono' or cmd == '--monospace'):
            out = convert(monospaceCharMap, text)
        if (cmd == '-b' or cmd == '--bold'):
            out = convert(boldCharMap, text)
        if (cmd == '-i' or cmd == '--italics'):
            out = convert(italicCharMap, text)
    elif(len(effects) < 3):
        cmd = effects[0]
        opt = effects[1]
        # Handle combinable effects
        if ((cmd == '-b' or cmd == '--bold') and
            (opt == '-s' or opt == '--sans')):
            out = convert(boldSansCharMap, text)
        if ((cmd == '-i' or cmd == '--italics') and
            (opt == '-b' or opt == '--bold')):
            out = convert(boldItalicCharMap, text)
        if ((cmd == '-i' or cmd == '--italics') and
            (opt == '-s' or opt == '--sans')):
            out = convert(boldItalicSansCharMap, text)
        if ((cmd == '-st' or cmd == '--strike') and opt == '-'):
            out = strikethrough(text, u'\u0336')
        if ((cmd == '-st' or cmd == '--strike') and opt == '~'):
            out = strikethrough(text, u'\u0334')
    print(out)
