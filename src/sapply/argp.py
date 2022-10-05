from loguru import logger
import typing, sys, inspect, os

# How the usage formatter will work
# Either:
# - Pass in format string with given help/usage format type
# - Use default formatting
# Parse format strings
# Replace tokens with variables & values, expand options
# Create print_usage(exit=EXIT_VALUE), where it does not exit on print_usage by default

# Forward Declarations of Types
# UsageFormatter = typing.NewType("UsageFormatter", None)
HelpFormatter = typing.NewType("HelpFormatter", None)

Option = typing.NewType("Option", None)
ArgParser = typing.NewType("ArgParser", None)
Command = typing.NewType("Command", ArgParser)
Argp = typing.NewType("Argp", ArgParser)

DEFAULT_HEADER_FORMAT: str = inspect.cleandoc(
    '''
    {prog}: {usage}
    {desc}\n
    {arg_defs}
    ''')
DEFAULT_INDICATOR = "Usage"

class HelpFormatter():
    # DEFAULT_HEADER_FORMAT: str = (
        # '{prog}: {usage}\n',
        # '{desc}\n\n',
        # '{arg_defs}\n',
    # )

    # def __init__(self, prog='', desc='', msg='', usage=DEFAULT_HEADER_FORMAT):
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
        # print(msg)

        # self.usage.clo
        # self.usage.replace("{prog}", prog)
        # self.usage.replace("{prog}", prog)

        options_msg: str = ''
        cmds_msg: str = ''

        arg_def: Command | Option
        # for arg_id, arg_def in argp.arg_defs:
        for arg_def in self.arg_defs:
        # for arg_id, arg_def in self.arg_defs:
            if isinstance(arg_def, Command):
                # Format commands like this for now:
                # id        help
                # TODO: Support sub options in commands
                # In the future, we want commands like
                # id        help
                #   short, long         help
                #   short, long         help
                pass
            elif isinstance(arg_def, Option):
                # Format options like:
                # {indent} short, long {help_indent} help
                # {indent}      , long {help_indent} help
                # {indent} short       {help_indent} help
                short = arg_def.short
                long = arg_def.long
                help = arg_def.help

                # indent = 2
                # help_indent = 27

                # format = f'{short:<indent}, {long} {help:>help_indent}'

                # format = f'{short:<2}, {long} {help:>22}\n'
                # format = f'{short:<2}, {long:<22} {help}\n'
                # format = f'{short:>2}, {long:<22} {help}\n'

                # format = f'{short:>2}, {long:<23}{help}\n'
                space = ' '
                comma = ','
                # format = f'{space:<2} {short}{comma:<2} {long:<23}{help}\n'

                # format = f'{space:<2} {short}, {long:>23}{help}\n'

                #   -v,  --version              Show program version
                #   -V,  --verbose              Enable verbose mode
                #   -sb, --sub                  Subscript text
                # format = f'{space:<2} {short}{comma:<2} {long:<23}{help}\n'

                # indent = f'{space:<2}'
                # flags = f'{short}{comma:<2}{long:<23}'

                # format = f'{indent}{flags}{help}'
                # format = f'{space:<2}{short}{comma:<2}{long:<23}{help}\n'
                short_flag = short + ','
                # format = f'{space:<2}{short_flag:<6}{long:<23}{help}\n'
                format = f'{space:<2}{short_flag:<6}{long:<21}{help}\n'

                options_msg += format
                # self.msg = format

        logger.debug(f'{prog=} {desc=} {usage=}')
        logger.debug(options_msg)

        # Format the message
        msg = msg.format(prog=prog, usage=usage, desc=desc, arg_defs=options_msg)
        # msg.format(prog)

        # msg.format(prog=self.prog,
                   # usage=self.usage,
                   # desc=self.desc,
                   # arg_defs=options_msg)

        # msg.format(self.prog, self.usage, self.desc, options_msg)
        # msg.replace('{prog}', prog)
        self.msg = msg

    # def get_msg(self):
        # return self.msg

    def show_usage(self):
        self.format_help()
        print(self.msg)
        # print(self.get_msg())
        sys.exit(1)

# Formatting
# class HelpFormatter():
    # DEFAULT_INDICATOR = "Usage"
    # DEFAULT_HEADER_FORMAT = (f'%s: %s\n',
                      # f'%s\n',)
    # # def __init__(self, usage, argp):
    # def __init__(self, argp: Argp):
        # format_string = ''
        # arg_def: Command | Option
        # # for arg_def in argp.arg_defs:
            # # arg_def.items()
        # for _, arg_def in argp.arg_defs:
            # if isinstance(arg_def, Command):
                # cmd: Command = arg_def
                # cmd.id
            # elif isinstance(arg_def, Option):
                # pass
            # pass
        # self.usage = UsageFormatter(self.DEFAULT_INDICATOR, "")

# class UsageFormatter():
    # def __init__(self, indicator, msg):
        # self.usage = (f'{indicator}: {msg}')
        # pass

class Option():
    def __init__(self, short: str, long: str, val='', flag=False, id='', callback: typing.Callable = lambda: None, help=''):
        self.id = id
        self.short = short
        self.long = long
        self.flag = flag
        self.val = val
        self.callback = callback
        self.help = help

        self.set_id()

    def set_id(self):
        ''' Sets the option id from the longname specifier
        and defaults to the shortname if not specified '''
        if self.long[0:1] == '--':
            self.id = self.long[1:]
        else:
            self.id = self.short[1:]

    def is_flag(self):
        return True if self.flag else False

class ArgParser():
    def __init__(self, argp_args: list, help='', *args, **kwargs):
        self.args = argp_args
        self.help = help

        # Initialize the keywords for easy matching
        self.arguments = []
        self.arg_defs: dict = {}
        self.arg_vals: dict = {}
        for arg in self.args:
            self.arg_defs[arg.id] = arg

        # Stores the values of the options & arguments

    def get_id(self, id):
        # Test for short option
        long = id[1:]
        short = id[0:]
        result: Command | Option | str
        if self.arg_defs.__contains__(id):
            result = self.arg_defs[id]
        if self.arg_defs.__contains__(long):
            result = self.arg_defs[long]
        elif self.arg_defs.__contains__(short):
            result = self.arg_defs[short]
        else:
            result = 'Argument ID Not Found'
        return result

    def parse(self, argvs: list):
        index = 1
        logger.debug('Parsing arguments')
        for argv in argvs:
            logger.debug(f'Arg #{index}: {argv}')
            arg: Command | Option | str = self.get_id(argv)

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
                    self.arg_vals[arg.id] = True if arg.is_flag() else arg
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
    def __init__(self, args: list, description='', no_help_message=False):
        if not no_help_message:
            # Init HelpFormatter
            prog = os.path.basename(__file__)
            usage = ''
            desc = description
            # print(f'{prog}, {usage}, {desc}')
            self.help = HelpFormatter(arg_defs=args, prog=prog, usage=usage, desc=desc)
            # self.help = HelpFormatter()

            # Add -h, --help option
            # show_help = lambda help: help.format_help(); help.show_usage()
            help_option = Option('-h', '--help', callback=self.help.show_usage, help='Show program usage')
            # help_option = Option('-h', '--help', callback=self.help, help='Show program usage')
            args.append(help_option)

        super().__init__(args)
        self.argv = sys.argv[1:]
        self.description = description

    def parse(self):
        super().parse(self.argv)
