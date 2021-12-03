from pathlib import Path
# from cmapdefs import *
from sap.cmapdefs import cmapdefs
from sap.charmap import read_charmap
import sys
# import re
from sap.flip import flip
from sap.zalgo import zalgo
from sap.morse import to_morse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

import pathlib

import site
def get_site_packages_dir():
    return [p for p  in site.getsitepackages()
            if "site-packages" in p][0]

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

def mapto(cmap: str):
    file = cmapdefs[cmap]
    # path = (f'{get_site_packages_dir()}resources/{file}')
    # path = (f'~/.local/lib/python3.9/site-packages/sap/resources/{file}')
    # path = Path(f'./resources/{file}')
    # path = pathlib.Path(f'~/.local/lib/python3.9/site-packages/sap/resources/{file}').expanduser()
    # root=get_site_packages_dir()
    # local=get_site_packages_dir()
    sitepkgs = site.getsitepackages()
    localsitepkgs = site.getusersitepackages()
    root    = Path(f'{sitepkgs}/sap')
    local   = Path(f'{localsitepkgs}/sap')
    path = ''
    if (root.is_dir()):
        path = pathlib.Path(f'{root}/resources/{file}').expanduser()
    else:
        path = pathlib.Path(f'{local}/resources/{file}').expanduser()
    return(read_charmap(path))

def main():
    cmds = ['flip', 'zalgo', 'morse']

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
            out = convert(mapto('subscriptCharMap'), text)
        if (optmatch(cmd, '--super')):
            out = convert(mapto('superscriptCharMap'), text)
        if (optmatch(cmd, '-ds', '--doublestruck')):
            out = convert(mapto('doubleStruckCharMap'), text)
        if (optmatch(cmd, '-oe', '--oldeng')):
            out = convert(mapto('oldEnglishCharMap'), text)
        if (optmatch(cmd, '-med', '--medieval')):
            out = convert(mapto('medievalCharMap'), text)
        if (optmatch(cmd, '-mono', '--monospace')):
            out = convert(mapto('monospaceCharMap'), text)
        if (optmatch(cmd, '-b', '--bold')):
            out = convert(mapto('boldCharMap'), text)
        if (optmatch(cmd, '-i', '--italics')):
            out = convert(mapto('italicCharMap'), text)
    elif(len(effects) < 3):
        cmd = effects[0]
        opt = effects[1]
        # convert([\a-zA-Z]*/convert(mapto())/g
        # Handle combinable effects
        if (optmatch(cmd, '--cmap')):
            opt = effects[1]
            cmap = read_charmap(opt)
            out = convert(cmap, text)
        if (optmatch(cmd, '-b', '--bold') and optmatch(opt, '-s', '--sans')):
            out = convert(mapto('boldSansCharMap'), text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-b', '--bold')):
            out = convert(mapto('boldItalicCharMap'), text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-s', '--sans')):
            out = convert(mapto('boldItalicSansCharMap'), text)
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '-')):
            out = strikethrough(text, u'\u0336')
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '~')):
            out = strikethrough(text, u'\u0334')
    print(out)
