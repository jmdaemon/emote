from cmapdefs import *
import sys
import re
from flip import flip
from zalgo import zalgo
from morse import to_morse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

MAJOR, MINOR, PATCH = '0', '1', '0'

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
    cmds = ['flip', 'zalgo', 'morse']

    # arg = sys.argv[1]
    # subcmd = arg
    # text = sys.argv[2]
    # effects = [subcmd,]

    # cmd = sys.argv[1]
    subcmd = None
    text = None
    effects = None

    for cmd in cmds:
        if cmd in sys.argv:
            subcmd = cmd

    if subcmd is None:
        text = sys.argv[1]
        effects = sys.argv[2:]
    else:
        text    = sys.argv[2]
        effects = sys.argv[3:]

    if not text:
        sys.exit()

    # Subcommands
    # Add subargs for each of these commands
    # Pass args parameter and parse commands in each function
    if (subcmd == 'flip'):
        flip(text)
    if (subcmd == 'zalgo'):
        zalgo(text)
    if (subcmd == 'morse'):
        print(to_morse(text.upper()))
    if (subcmd is not None):
        return

    # Main
    out = ""
    if(len(effects) < 2):
        cmd = effects[0]
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
