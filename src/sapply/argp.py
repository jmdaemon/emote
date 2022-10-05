import typing, sys, inspect, os
from loguru import logger

# TODO:
    # - Fix long & short options not working
    # - Refactor program to use 'val' option field
    # - Only source of arguments is in the options list
    # Argp:
    # - Flesh out rest of the support for subcommands
    # - Add subcommand options
    # - Add support for parsing multiple options & text
    # - Move argp declaration to separate python module
    # - Add callbacks with arguments feature
    # - Write unit tests, documentation, create package, upload

# Forward Declarations of Types
HelpFormatter = typing.NewType("HelpFormatter", None)

Option = typing.NewType("Option", None)
ArgParser = typing.NewType("ArgParser", None)
Command = typing.NewType("Command", ArgParser)
Argp = typing.NewType("Argp", ArgParser)

class HelpFormatter():
    DEFAULT_HEADER_FORMAT: str = inspect.cleandoc(
        '''
        {prog}: {usage}
        {desc}\n
        {arg_defs}
        ''')
    DEFAULT_INDICATOR = "Usage"

    def __init__(self, arg_defs, prog='', usage='', desc='', usage_format=DEFAULT_HEADER_FORMAT):
        self.arg_defs = arg_defs
        self.prog = prog
        self.usage = usage
        self.desc = desc
        self.usage_format = usage_format
        self.msg = ''

    def format_help(self):
        prog = self.prog
        usage = self.usage
        desc = self.desc

        arg_defs = ''

        # Keep usage_format intact
        msg = self.usage_format[:]

        options_msg: str = ''
        cmds_msg: str = ''

        arg_def: Command | Option
        for arg_def in self.arg_defs:
            if isinstance(arg_def, Command):
                # Format commands like this for now:
                # id        help
                # TODO: Support sub options in commands
                # In the future, we want commands like
                # id        help
                #   short, long         help
                #   short, long         help
                format = ''
                cmds_msg += format
            elif isinstance(arg_def, Option):
                # Default option format:
                #   -v,  --version              Show program version
                #   -sb, --sub                  Subscript text
                space = ' '
                short = arg_def.short
                long = arg_def.long
                help = arg_def.help

                short_flag = short + ','
                format = f'{space:<2}{short_flag:<6}{long:<21}{help}\n'

                options_msg += format

        logger.debug(f'{prog=} {desc=} {usage=}')
        logger.debug(cmds_msg)
        logger.debug(options_msg)

        # Format the message
        arg_defs = cmds_msg + '\n' + options_msg if cmds_msg != '' else options_msg
        msg = msg.format(prog=prog, usage=usage, desc=desc, arg_defs=arg_defs)
        self.msg = msg

    def show_usage(self):
        self.format_help()
        print(self.msg)
        sys.exit(1)

class Option():
    # def __init__(self, short: str, long: str, val='', flag=False, id='', callback: typing.Callable = lambda: None, help=''):
    def __init__(self, short: str, long: str, val='', flag=False, id='', callback: typing.Callable = None, help=''):
        self.short = short
        self.long = long
        self.val = val
        self.flag = flag
        # self.id = id
        # short -> id
        # long -> id
        self.ids: dict[str, str] = {}
        self.callback = callback
        self.help = help

        self.set_id()

    def set_id(self):
        ''' Sets the option id from the longname specifier
        and defaults to the shortname if not specified '''
        # long_hypen = 
        # short_hypen = self.short[0:1]
        if self.long[0:2] == '--':
            # print(self.long)
            # self.id = self.long[1:]
            # self.id = self.long[2:]
            self.ids[self.long] = self.long[2:]
        # self.id = self.short[1:]
        # self.id = self.short[1:]
        self.ids[self.short] = self.short[1:]
        # else:
        # print(self.id)

    def is_flag(self):
        return True if self.flag else False

class ArgParser():
    def __init__(self, argp_args: list[Command | Option], help='', *args, **kwargs):
        self.args = argp_args
        self.help = help

        # Initialize the keywords for easy matching
        self.arguments: list[str] = []
        self.arg_defs: dict = {}
        self.arg_vals: dict = {}
        # logger.debug('ArgParser __init__')
        for arg in self.args:
            if isinstance(arg, Option):
                ids_dict = arg.ids
                for flag, id in ids_dict.items():
                    logger.debug(f'{flag=}, {id=}')
                    # self.arg_defs[id] = flag
                    # self.arg_defs[flag] = id
                    self.arg_defs[id] = arg

            elif isinstance(arg, Command):
                self.arg_defs[arg.id] = arg
            # arg_id = self.args[
            # self.arg_defs[arg] = arg

            # self.arg_defs[arg.id] = arg

        # Stores the values of the options & arguments

    def get_id(self, id):
        # Test for short option
        # short = id[0:]

        long = id[2:]
        short = id[1:]
        result: Command | Option | str
        if self.arg_defs.__contains__(id): # Command
            result = self.arg_defs[id]
        elif self.arg_defs.__contains__(long): # Long option
            result = self.arg_defs[long]
        elif self.arg_defs.__contains__(short): # Short option
            result = self.arg_defs[short]
        else:
        # result: Command | Option | str
        # if self.arg_defs.__contains__(id):
            # result = self.arg_defs[id]
        # else:
            result = 'Argument ID Not Found'
        return result

    def parse(self, argvs: list):
        index = 1
        logger.debug('Parsing arguments')
        for argv in argvs:
            logger.debug(f'Arg #{index}: {argv}')
            # e.g: morse (cmd), i (short), italic (long), 'Argument ID Not Found' (argument)
            arg: Command | Option | str = self.get_id(argv)
            logger.debug(f'{arg=}')

            if isinstance(arg, Command):
                logger.debug('Is Command')
                if arg.callback != None:
                    arg.callback()
                else:
                    arg.parse(argv[index:])
            elif isinstance(arg, Option):
                logger.debug('Is Option')
                if arg.callback != None:
                    arg.callback()
                else:
                    # Index using the id, italic
                    # self.arg_vals[arg.id] = True if arg.is_flag() else arg
                    arg_id = arg.ids[argv]
                    self.arg_vals[arg_id] = True if arg.is_flag() else arg
            else:
                # Assume we are only left with an argument
                logger.debug('Is Argument')
                self.arguments.append(argv)
            index += 1

class Command(ArgParser):
    ''' Execute CLI Subcommands
    Commands should be able to:
        - Have separate options, arguments, flags, subcommands separate from the main program.
        - Execute callback functions
    '''
    def __init__(self, id: str, argp_args: list, callback: typing.Callable, help='', *args, **kwargs):
        super().__init__(argp_args)
        self.id = id
        self.callback = callback
        self.help = help

'''
Highly customizeable cli arguments parser

This argument parsing library was created to address flaws in argparse,
and direct parsing from sys.argv.

Some gripes that I've found when using argparse are:
    - Usage and other docstring names aren't capitalized, and are unable to be modified.
    - Does not accept '-' or '--' as valid arguments (arguments will be "unknown" and will show the usage message)
    - Only one subcommand/callback can be executed

When doing direct custom parsing from sys.argv:
    - Lots of tedious work to check inputs
    - No help/usage string by default
    - Awkward inputs & input handling
    - Specific to your project/no code reuse between programs

'''
class Argp(ArgParser):
    def __init__(self, args: list, usage='', desc='', help_formatter=None):
        if help_formatter == None:
            self.help = HelpFormatter(arg_defs=args, prog=os.path.basename(__file__), usage=usage, desc=desc)

            # Add -h, --help option
            # TODO: Long options are broken
            help_option = Option('-h', '--help', callback=self.help.show_usage, help='Show program usage')
            args.append(help_option)

        super().__init__(args)
        self.argv = sys.argv[1:]
        self.desc = desc

    def parse(self):
        super().parse(self.argv)
