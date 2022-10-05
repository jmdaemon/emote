# Sapply libraries
from sapply.argp import Command, Option, Argp
from sapply.cmap import to_charmap
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

TILDE_STRIKETHROUGH = u'\u0334'
HYPEN_STRIKETHROUGH = u'\u0336'

def strikethrough(text, strikeover=HYPEN_STRIKETHROUGH):
    ''' Converts ASCII characters into unicode 'striked' characters '''
    return ''.join([char + strikeover for char in text])

def mapto(cmap: str):
    ''' Maps ASCII characters to a unicode character map '''
    # file = cmapdefs[cmap]
    file = f'{cmap}.json'
    conts = pkg_resources.resource_string('sapply.resources', file)
    logger.debug(f'Resource File Contents:\n{conts}')
    return (to_charmap(conts))

def apply_effects(effect: str, text: str, cmap: str = '') -> str:
    ''' Applies unicode character mappings to ASCII text '''
    out = ''
    # opt = HYPEN_STRIKETHROUGH if (opt == '-') else TILDE_STRIKETHROUGH
    logger.debug('In match_effects:')
    if (cmap == ''):
        return out

    match effect:
        case '-st'  | '--strike':
            # TODO: Implement strikethrough with tilde, or hypen,
            # Maybe reimplement this as a command?
            out = strikethrough(text)
        case _: out = convert(mapto(cmap), text)
    return out

def show(text: str):
    ''' Displays the mapped text without the newline ending '''
    print(text, end='\0') # Strip newlines from text

def build_cli():
    ''' Creates the command line interface '''
    # TODO: Add flag option to disable capitlization of {prog} in program description
    PROGRAM_DESCRIPTION = '{prog} - Convert ASCII text to Unicode values'
    PROGRAM_USAGE = '{prog} [COMMAND...] [OPTIONS...] [text]'

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
        Option('-sb', '--sub'           , 'subscripts'      , help='Subscript text'),
        Option('-sp', '--super'         , 'superscripts'    , help='Superscript text'),
        Option('-st', '--strike'        , help='Strikethrough text'),
        Option('-ds', '--double-struck' , 'doublestruck'    , help='Double struck/Blackboard bold text'),
        Option('-oe', '--oldeng'        , 'old-eng'         , help='Old English style text'),
        Option('-me', '--medieval'      , 'med'             , help='Medieval style text'),
        Option('-mo', '--monospace'     , 'monospace'       , help='Monospace font text'),
        Option('-b' , '--bold'          , 'bold'            , help='Bold text'),
        Option('-bs', '--bold-sans'     , 'bold-sans'       , help='Bold sans-serif text'),
        Option('-i' , '--italic'        , 'italic'          , help='Italicized text'),
        Option('-ib', '--italic-bold'   , 'bold-italic'     , help='Italic bold text'), # Note: The h character is missing
        Option('-is', '--italic-sans'   , 'italic-sans'     , help='Italic sans-serif text'),
    ]

    argp = Argp(options, usage=PROGRAM_USAGE, desc=PROGRAM_DESCRIPTION)
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
    logger.debug(argp.arg_vals)

    out: str = ''
    # For all options set
    for _, val in argp.arg_vals.items():
        key_id = val.short
        cmap = val.val
        # cmap = argp.arg_defs[key_id].val
        # cmap = argp.get_id(key_id).val
        logger.debug(f'{cmap=}')
        # out = match_effects(key_id, text)
        out = apply_effects(key_id, text, cmap)
        if (out != ''):
            show(out)
