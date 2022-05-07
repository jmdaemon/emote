# Sapply libraries
from sapply.cmapdefs import cmapdefs
from sapply.charmap import to_charmap
from sapply.flip import flip
from sapply.zalgo import zalgo
from sapply.morse import to_morse
from sapply.tokens import to_string,parse_transforms
from sapply import __version__

# Standard library
import os
import re
import sys
import logging
from pkg_resources import resource_string
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

def convert(char_map, text):
    ''' Convert characters from ASCII to a specific unicode character map '''
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
    ''' Converts ASCII characters into unicode 'striked' characters '''
    return ''.join([char + strikeover for char in text])

def mapto(cmap: str):
    ''' Maps ASCII characters to a unicode character map '''
    file = cmapdefs[cmap]
    conts = resource_string('sapply.resources', file)
    logging.debug(f'Resource File Contents:\n{conts}')
    return (to_charmap(conts))

def match_effects(cmd: str, text: str, opt=None) -> str:
    ''' Applies unicode character mappings to ASCII text '''
    out = ''
    opt = u'\u0336' if (opt == '-') else u'\u0334' # - or ~ strikethrough
    logging.debug('In match_effects:')

    match cmd:
        case '--sub'                        : out = convert(mapto('subscript'), text)
        case '--super'                      : out = convert(mapto('superscript'), text)
        case '-ds'      | '--doublestruck'  : out = convert(mapto('doubleStruck'), text)
        case '-oe'      | '--oldeng'        : out = convert(mapto('oldEnglish'), text)
        case '-med'     | '--medieval'      : out = convert(mapto('medieval'), text)
        case '-mono'    | '--monospace'     : out = convert(mapto('monospace'), text)
        case '-b'       | '--bold'          : out = convert(mapto('bold'), text)
        case '-i'       | '--italics'       : out = convert(mapto('italic'), text)
        case '-bs'  | '--boldsans'          : out = convert(mapto('boldSans'), text)
        case '-ib'  | '--italicbold'        : out = convert(mapto('boldItalic'), text)
        case '-is'  | '--italicsans'        : out = convert(mapto('italicSans'), text)
        case '-st'  | '--strike'            : out = strikethrough(text, opt)
    return out

def main():
    ''' Main application entry point

    Usage:
        sapply asdf -i
        sapply asdf -is
        sapply asdf -cmap ./cmap.json
    '''
    loglevel = os.environ.get("LOGLEVEL")
    loglevel = loglevel if loglevel is not None else logging.ERROR
    logging.basicConfig(level=loglevel)

    cmds = ['flip', 'zalgo', 'morse']

    subcmd = None
    text = None
    effects = None

    i = 0
    for cmd in cmds:
        if cmd in sys.argv:
            subcmd = cmd
        if sys.argv[i] == "-v":
            print(f'sapply v{__version__}')
            exit(0)
        i += 1

    if subcmd is None:
        text = sys.argv[1]
        effects = sys.argv[2:]
    else:
        text    = sys.argv[2]
        effects = sys.argv[3:]

    logging.info(f'Subcommand   : {subcmd}')
    logging.info(f'Text         : {text}')
    logging.info(f'Effects      : {effects}')

    if not text:
        sys.exit()

    # Subcommands
    match subcmd:
        case 'flip'     : flip(text)
        case 'zalgo'    : zalgo(text)
        case 'morse'    : print(to_morse(text.upper())) # TODO: Pass `effects` off to function for processing

    out = ''
    if (len(effects) < 2):
        logging.debug('Non-combinable effect')
        cmd = effects[0]
        out = match_effects(cmd, text)
        logging.debug(f'Effect: {cmd}')

    elif (len(effects) < 3):
        logging.debug('Combinable effect')
        cmd = effects[0]
        opt = effects[1]
        logging.debug(f'Effect: {cmd}')
        logging.debug(f'Option: {opt}')
        if (opt is None):
            opt = re.match(re.compile(r'-st='), cmd)
        # Handle combinable effects
        match cmd, opt:
            case '--cmap', _:
                cmap = read_charmap(opt)
                out = convert(cmap, text)
            case '-f', _:
                # opt == fp
                token_dict = parse_transforms(opt)
                for effect, text in token_dict.items():
                    if (text == '\n'):
                        out += '\n'
                    else:
                        out += match_effects(effect, text) + ' '
            case _,_: out = match_effects(effect, text, opt)
    print(out)
