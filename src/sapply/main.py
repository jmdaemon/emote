# Sapply libraries
from sapply.argp import Command, Option, Argp
from sapply.cmap import cmapdefs, to_charmap
from sapply.flip import flip
from sapply.zalgo import zalgo
from sapply.morse import to_morse
from sapply.tokens import parse_transforms
from sapply import __version__

# Third Party Libraries
from wora.cli import reset_sigpipe_handling
from loguru import logger

# Standard library
import argparse, typing, pkg_resources, os, re, sys

reset_sigpipe_handling()

def convert(char_map, text):
    ''' Convert characters from ASCII to a specific unicode character map '''
    out = ''
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
    conts = pkg_resources.resource_string('sapply.resources', file)
    logger.debug(f'Resource File Contents:\n{conts}')
    return (to_charmap(conts))

def match_effects(cmd: str, text: str, opt=None) -> str:
    ''' Applies unicode character mappings to ASCII text '''
    out = ''
    opt = u'\u0336' if (opt == '-') else u'\u0334' # - or ~ strikethrough
    logger.debug('In match_effects:')

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

def show(text: str):
    ''' Displays the mapped text without the newline ending '''
    print(text, end='\0') # Strip newlines from text

def build_cli():
    PROGRAM_DESCRIPTION = 'Convert ASCII text to Unicode values'

    morse_options = [
        Option('-m', '--morse', 'Convert text to Morse code'),
        Option('-a', '--ascii', 'Convert text to ASCII text'),
    ]

    options = [
        # Commands
        Command('flip', list(), lambda x: x, help=''),
        Command('morse', morse_options, lambda x: x, help=''),
        Command('zalgo', list(), lambda x: x, help=''),
        # Normal CLI Options
        # Note that -h, --help option should be specified.
        Option('-v', '--version'        , help='Show program version'),
        Option('-V', '--verbose'        , help='Enable verbose mode'),
        # Format Options
        # Option('-e', '--effect', 'Applies an effect on the text. '),
        Option('-sb', '--sub'           , help='Subscript text'),
        Option('-sp', '--super'         , help='Superscript text'),
        Option('-st', '--strike'        , help='Strikethrough text'),
        Option('-oe', '--oldeng'        , help='Old English style text'),
        Option('-me', '--medieval'      , help='Medieval style text'),
        Option('-mo', '--monospace'     , help='Monospace font text'),
        Option('-b' , '--bold'          , help='Bold text'),
        Option('-bs', '--bold-sans'     , help='Bold sans-serif text'),
        Option('-i' , '--italic'        , help='Italicized text'),
        Option('-ib', '--italic-bold'   , help='Italic bold text'),
        Option('-is', '--italic-sans'   , help='Italic sans-serif text'),
    ]

    argp = Argp(options, description=PROGRAM_DESCRIPTION)
    return argp

def main():
    ''' Main application entry point

    Usage:
        sapply asdf -i
        sapply asdf -is
        sapply asdf -cmap ./cmap.json
    '''
    logger.remove() # Override default logger
    # Format: [2022-09-01 23:36:01.792] [DEBUG] [bin_name.main:150] Hello!
    PROGRAM_LOG_MSG_FORMAT = '\x1b[0m\x1b[32m[{time:YYYY-MM-DD HH:mm:ss.SSS}]\x1b[0m [<lvl>{level}</>] [<c>{name}:{line}</>] {message}'
    loglevel = 'ERROR' if os.environ.get('LOGLEVEL') is None else os.environ.get('LOGLEVEL')
    logger.add(sys.stdout, format=PROGRAM_LOG_MSG_FORMAT, level=loglevel)

    argp = build_cli()
    argp.parse()

    text = argp.arguments[0]

    out: str = ''
    for _, val in argp.arg_vals.items():
        key_id = val.short
        out = match_effects(key_id, text)
    show(out)

