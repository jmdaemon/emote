# Sapply libraries
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

# Reasons why I don't like argparse
# usage and other names aren't capitalized.
# cannot accept '-' or '--' as arguments 
# only one operation/subcommand can be processed at a time

# Reasons why I don't like custom parsing
# no help/usage string
# awkward inputs and input handling
# lack of code reuse between projects

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

# Argp
class Option():
    def __init__(self, short: str, long: str, val='', flag=False, id='', help=''):
        self.id = id
        self.short = short
        self.long = long
        self.flag = flag
        self.val = val
        self.help = help

        # Default setting of id
        # TODO: Chop off the leading -- for long options properly
        if long != None:
            self.id = long[1:]

class Command():
    # Commands
    # Should be able to:
        # - Specify their own arguments, options, further subcommands
        # - Specify and execute custom callback with their specified options
        # - Embed themselves in other commands
    def __init__(self, invoke: str, options: list[Option], callback: typing.Callable, help=''):
        self.invoke = invoke
        self.callback = callback
        self.options = options
        self.help = help

        # Initialize the keywords for easy matching
        self.keynames: dict = {}
        for arg in self.options:
            if isinstance(arg, Command):
                self.keynames[arg.invoke] = arg
            elif isinstance(arg, Option):
                self.keynames[arg.id] = arg
        self.keyvalues: dict = {}
        self.arguments = []

    def parse(self, argv):
        index = 0
        for argv in argv:
            if self.keynames.__contains__(argv):
                arg: Command | Option = self.keynames[argv]
                if isinstance(arg, Command):
                    if arg.callback != None:
                        arg.callback()
                    else:
                        arg.parse(argv[index:])
                elif isinstance(arg, Option):
                    # Set the value of the option if any
                    # If option == flag, toggle flag value
                    # Set option in main 
                    if arg.flag:
                        self.keyvalues[arg.id] = True
                    else:
                        self.keyvalues[arg.id] = arg.val
                else:
                    # Assume we are only left with an argument
                    self.arguments.append(arg)
            index += 1

class Argp:
    def __init__(self, args: list, description=''):
        self.args = args
        self.argv = sys.argv[1:]
        self.description = description

        # Initialize the keywords for easy matching
        self.keynames: dict = {}
        for arg in self.args:
            if isinstance(arg, Command):
                self.keynames[arg.invoke] = arg
            # TODO: Create option mapping where short, long options could match id
            elif isinstance(arg, Option):
                # self.keynames[arg.id] = arg
                self.keynames[arg.short] = arg

        print(self.keynames)

        # Stores the values of the options
        self.keyvalues: dict = {}
        self.arguments = []

    def parse(self):
        index = 1
        for argv in self.argv:
            print(argv)
            if self.keynames.__contains__(argv):
                print("Running")
                arg: Command | Option = self.keynames[argv]
                print(f"arg: {arg}")
                if isinstance(arg, Command):
                    print("Argument is a Command")
                    if arg.callback != None:
                        arg.callback()
                    else:
                        # TODO: Recursively parse the damn thing
                        arg.parse(self.argv[index:])
                    continue
                elif isinstance(arg, Option):
                    print("Argument is an Option")
                    # Set the value of the option if any
                    # If option == flag, toggle flag value
                    # Set option in main 
                    if arg.flag:
                        self.keyvalues[arg.id] = True
                    else:
                        # self.keyvalues[arg.id] = arg.val
                         self.keyvalues[arg.id] = argv
                         # self.keyvalues[arg.short] = argv
                    continue
            else:
                print("Argument is an Argument")
                # Assume we are only left with an argument
                print("Initializing arg")
                self.arguments.append(argv)
            index += 1

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
        Option('-v', '--version'        , 'Show program version'),
        Option('-V', '--verbose'        , 'Enable verbose mode'),
        # Format Options
        # Option('-e', '--effect', 'Applies an effect on the text. '),
        Option('-sb', '--sub'           , 'Subscript text'),
        Option('-sp', '--super'         , 'Superscript text'),
        Option('-st', '--strike'        , 'Strikethrough text'),
        Option('-oe', '--oldeng'        , 'Old English style text'),
        Option('-me', '--medieval'      , 'Medieval style text'),
        Option('-mo', '--monospace'     , 'Monospace font text'),
        Option('-b' , '--bold'          , 'Bold text'),
        Option('-bs', '--bold-sans'     , 'Bold sans-serif text'),
        Option('-i' , '--italic'        , 'Italicized text'),
        Option('-ib', '--italic-bold'   , 'Italic bold text'),
        Option('-is', '--italic-sans'   , 'Italic sans-serif text'),
    ]

    argp = Argp(options, description=PROGRAM_DESCRIPTION)
    argp.parse()

    print(argp.keyvalues)
    text = argp.arguments[0]

    out: str = ''
    # for key, _ in argp.keyvalues.items():
    for key, val in argp.keyvalues.items():
        # print(key)
        # print(val)
        out = match_effects(argp.keyvalues[key], text)
    show(out)
    # Apply only the last effect specified
    # cmds = ['flip', 'zalgo', 'morse']

    # subcmd = None
    # text = None
    # effects = None

    # i = 0
    # for cmd in cmds:
        # if cmd in sys.argv:
            # subcmd = cmd
        # if sys.argv[i] == "-v":
            # print(f'sapply v{__version__}')
            # exit(0)
        # i += 1

    # if subcmd is None:
        # text = sys.argv[1]
        # effects = sys.argv[2:]
    # else:
        # text    = sys.argv[2]
        # effects = sys.argv[3:]

    # logger.info(f'Subcommand   : {subcmd}')
    # logger.info(f'Text         : {text}')
    # logger.info(f'Effects      : {effects}')

    # if not text:
        # sys.exit()

    # # Subcommands
    # match subcmd:
        # case 'flip'     : show(flip(text))
        # case 'zalgo'    : show(zalgo(text))
        # case 'morse'    : show(to_morse(text.upper())) # TODO: Pass `effects` off to function for processing
    # # If a subcommand is used
    # if subcmd is not None:
        # # Exit early
        # return

    # out = ''
    # if (len(effects) < 2):
        # logger.debug('Non-combinable effect')
        # cmd = effects[0]
        # out = match_effects(cmd, text)
        # logger.debug(f'Effect: {cmd}')

    # elif (len(effects) < 3):
        # logger.debug('Combinable effect')
        # cmd = effects[0]
        # opt = effects[1]
        # logger.debug(f'Effect: {cmd}')
        # logger.debug(f'Option: {opt}')
        # if (opt is None):
            # opt = re.match(re.compile(r'-st='), cmd)
        # # Handle combinable effects
        # match cmd, opt:
            # case '--cmap', _:
                # cmap = read_charmap(opt)
                # out = convert(cmap, text)
            # case '-f', _:
                # # opt == fp
                # token_dict = parse_transforms(opt)
                # for effect, text in token_dict.items():
                    # if (text == '\n'):
                        # out += '\n'
                    # else:
                        # out += match_effects(effect, text) + ' '
            # case _,_: out = match_effects(effect, text, opt)
    # show(out)
