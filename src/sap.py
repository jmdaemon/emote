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

def optmatch(cmd, short, long=''):
    if (long == ''):
        return (cmd == short)
    else:
        return (cmd == short or cmd == long)

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
        if (optmatch(cmd, 'v', '--version')):
            MAJOR, MINOR, PATCH = '0', '1', '0'
            print(f'strmanip - v{MAJOR}.{MINOR}.{PATCH}')
            sys.exit()
        if (optmatch(cmd, '--sub')):
            out = convert(subscriptCharMap, text)
        if (optmatch(cmd, '--super')):
            out = convert(superscriptCharMap, text)
        if (optmatch(cmd, '-ds', '--doublestruck')):
            out = convert(doubleStruckCharMap, text)
        if (optmatch(cmd, '-oe', '--oldeng')):
            out = convert(oldEnglishCharMap, text)
        if (optmatch(cmd, '-med', '--medieval')):
            out = convert(medievalCharMap, text)
        if (optmatch(cmd, '-mono', '--monospace')):
            out = convert(monospaceCharMap, text)
        if (optmatch(cmd, '-b', '--bold')):
            out = convert(boldCharMap, text)
        if (optmatch(cmd, '-i', '--italics')):
            out = convert(italicCharMap, text)
    elif(len(effects) < 3):
        cmd = effects[0]
        opt = effects[1]
        # Handle combinable effects
        if (optmatch(cmd, '-b', '--bold') and optmatch(opt, '-s', '--sans')):
            out = convert(boldSansCharMap, text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-b', '--bold')):
            out = convert(boldItalicCharMap, text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-s', '--sans')):
            out = convert(boldItalicSansCharMap, text)
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '-')):
            out = strikethrough(text, u'\u0336')
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '~')):
            out = strikethrough(text, u'\u0334')
    print(out)
