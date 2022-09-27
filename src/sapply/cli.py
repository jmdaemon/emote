# Sapply libraries
from sapply.cmapdefs import cmapdefs
from sapply.charmap import to_charmap
from sapply.flip import flip
from sapply.zalgo import zalgo
from sapply.morse import to_morse
from sapply.tokens import to_string,parse_transforms
from sapply import __version__

# Third Party Libraries
from wora.cli import reset_sigpipe_handling
from loguru import logger

# Standard library
import pkg_resources, os, re, sys

reset_sigpipe_handling()

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

    logger.info(f'Subcommand   : {subcmd}')
    logger.info(f'Text         : {text}')
    logger.info(f'Effects      : {effects}')

    if not text:
        sys.exit()

    # Subcommands
    match subcmd:
        case 'flip'     : show(flip(text))
        case 'zalgo'    : show(zalgo(text))
        case 'morse'    : show(to_morse(text.upper())) # TODO: Pass `effects` off to function for processing
    # If a subcommand is used
    if subcmd is not None:
        # Exit early
        return

    out = ''
    if (len(effects) < 2):
        logger.debug('Non-combinable effect')
        cmd = effects[0]
        out = match_effects(cmd, text)
        logger.debug(f'Effect: {cmd}')

    elif (len(effects) < 3):
        logger.debug('Combinable effect')
        cmd = effects[0]
        opt = effects[1]
        logger.debug(f'Effect: {cmd}')
        logger.debug(f'Option: {opt}')
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
    show(out)
