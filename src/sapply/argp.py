import typing, sys, inspect, os
from loguru import logger

# TODO:
    # - Only source of arguments is in the options list
    # Argp:
    # Priority
        # - Add subcommand options
        # - Add callbacks with arguments feature
        # - Add support for options with nargs, + specify strings for options
        #   - Create type option to specify arg type, and ensure that an arg value
        #       is given for it in ArgParser.parse()
    # - Flesh out rest of the support for subcommands
    # - Add support for parsing multiple options & text
    # - Move argp declaration to separate python module
    # - Write unit tests, documentation, create package, upload

# Forward Declarations of Types
HelpFormatter = typing.NewType("HelpFormatter", None)

Option = typing.NewType("Option", None)
ArgParser = typing.NewType("ArgParser", None)
Command = typing.NewType("Command", ArgParser)
Argp = typing.NewType("Argp", ArgParser)

def map_cli_id_defs(cli: list[Command | Option]):
    '''
    Maps the the command line interface definitions to a known identifier that
        will be compared with arguments given to a program.
    TODO:
        Add feature to disable matching option-command identifier names
    '''
    defs = {}
    for cli_def in cli:
        if isinstance(cli_def, Option):
            ids_dict = cli_def.ids
            for flag, id in ids_dict.items():
                logger.debug(f'{flag=}, {id=}')
                defs[id] = cli_def
        elif isinstance(cli_def, Command):
            defs[cli_def.id] = cli_def

    return defs

class OptionsFormatter():
    ''' Formats command line options '''
    def __init__(self, argp_args: list,
                 format='{space:<{indent}}{short_flag:<{short_padding}}{long:<{long_padding}}{help}\n',
                 indent=2, short_padding=6, long_padding=21, *args, **kwargs):
        self.args = argp_args
        self.format = format
        self.indent = indent
        self.format = format
        self.short_padding = short_padding
        self.long_padding = long_padding
        self.msg = ''

    def format_help(self):
        for arg in self.args:
            if isinstance(arg, Option):
                # Default option format:
                #   -v,  --version              Show program version
                #   -sb, --sub                  Subscript text
                self.msg += self.format.format(
                    space=' ', indent=self.indent,
                    short_padding=self.short_padding, long_padding=self.long_padding,
                    short_flag=arg.short + ',', long=arg.long, help=arg.help)
        return self.msg

class HelpFormatter():
    DEFAULT_HEADER_FORMAT: str = inspect.cleandoc(
        '''
        {usage_indicator}: {usage}
        {desc}\n
        {arg_defs}
        ''')
    DEFAULT_INDICATOR = 'Usage'

    def __init__(self, arg_defs, prog='', usage='', desc='',
                 options_formatter = None,
                 usage_indicator=DEFAULT_INDICATOR, usage_format=DEFAULT_HEADER_FORMAT):
                 # indent=2,
                 # short_padding=6,
                 # long_padding=21,
        self.arg_defs = arg_defs
        self.prog = prog
        self.usage = usage
        self.desc = desc
        self.msg = ''

        # Format
        self.options_formatter = OptionsFormatter(arg_defs) if options_formatter is None else options_formatter
        self.usage_indicator = usage_indicator
        self.usage_format = usage_format

    def format_help(self):
        prog = self.prog
        usage_indicator = self.usage_indicator
        usage = self.usage
        desc = self.desc

        arg_defs = ''

        # Copy usage_format, usage strings
        usage_msg = self.usage[:]
        desc_msg = self.desc[:]
        msg = self.usage_format[:]

        options_msg: str = ''
        cmds_msg: str = ''

        arg_def: Command | Option
        # TODO: Ideal command default format
        # Command Format:
        # command-to-option:
        # id                    help
        #   short, long         help
        #   short, long         help
        # command-to-command:
        # id        help
        #   short, long         help
        #   id        help
        #       short, long         help

        for arg_def in self.arg_defs:
            # TODO: This solution only parses one layer of options for commands
            # TODO: Ideally this would recursively parse all command options
            if isinstance(arg_def, Command):
                space = ' '
                id = arg_def.id
                help = arg_def.help

                format = ''
                format = f'{space:<2}{id:<27}{help}'
                cmds_msg += format

                cmd_options_msg = ''
                # TODO: Refactor this
                for cmd_arg_def in arg_def.args:
                    if isinstance(cmd_arg_def, Option):
                        space = ' '
                        short = cmd_arg_def.short
                        long = cmd_arg_def.long
                        help = cmd_arg_def.help

                        short_flag = short + ','
                        # TODO: These should not be hardcoded
                        format = f'{space:<4}{short_flag:<6}{long:<19}{help}\n'
                        cmd_options_msg += format
                cmds_msg +=  '\n' + cmd_options_msg + '\n'

        options_msg += self.options_formatter.format_help()

        logger.debug(f'{prog=} {desc=} {usage=}')
        logger.debug(cmds_msg)
        logger.debug(options_msg)

        # Format the help message
        usage_msg = usage_msg.format(prog=prog)
        desc_msg = desc_msg.format(prog=prog.capitalize())

        arg_defs = 'Commands\n' + cmds_msg + 'Options\n' + options_msg if cmds_msg != '' else options_msg
        msg = msg.format(usage_indicator=usage_indicator, usage=usage_msg, desc=desc_msg, arg_defs=arg_defs)

        msg = msg.rstrip() # Remove last newline
        self.msg = msg

    def show_usage(self):
        self.format_help()
        print(self.msg)
        sys.exit(1)


# A single component definition used for all options, and commands
# class Comp():
    # ''' Component common to all '''
    # def __init__(self, id='', val='', flag=False, cb: typing.Callable = None, help=''):
        # self.id = id
        # self.val = val
        # self.flag = flag
        # self.ids: dict[str, str] = {}
        # self.callback = cb
        # self.help = help

class Option():
    def __init__(self, short: str, long: str, val='', flag=False, id='', cb: typing.Callable = None, help=''):
        self.short = short
        self.long = long
        self.flag = flag
        self.val = val
        self.ids: dict[str, str] = {}
        self.callback = cb
        self.help = help
        self.set_id()

    def set_id(self):
        ''' Sets the option id from the longname specifier
        and defaults to the shortname if not specified '''

        if self.long[0:2] == '--':
            self.ids[self.long] = self.long[2:]
        self.ids[self.short] = self.short[1:]

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
        self.arg_defs = map_cli_id_defs(self.args)

    def get_id(self, id):
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
            result = 'Argument ID Not Found'
        return result

def argp_parse(argp: ArgParser, argvs: list):
    ''' Parses the given command line arguments '''
    index = 1
    logger.debug('Parsing arguments')
    for argv in argvs:
        logger.debug(f'Arg #{index}: {argv}')
        # e.g: morse (cmd), i (short), italic (long), 'Argument ID Not Found' (argument)
        arg: Command | Option | str = argp.get_id(argv)
        logger.debug(f'{arg=}')

        if isinstance(arg, Command):
            logger.debug('Is Command')
            if arg.callback != None:
                arg.callback()
            else:
                argp_parse(argp, argv[index:])
        elif isinstance(arg, Option):
            logger.debug('Is Option')
            if arg.callback != None:
                arg.callback()
            else:
                # Index using the id, italic
                # self.arg_vals[arg.id] = True if arg.is_flag() else arg
                arg_id = arg.ids[argv]
                argp.arg_vals[arg_id] = True if arg.is_flag() else arg
        else:
            # Assume we are only left with an argument
            logger.debug('Is Argument')
            argp.arguments.append(argv)
        index += 1


class Command(ArgParser):
    ''' Execute CLI Subcommands
    Commands should be able to:
        - Have separate options, arguments, flags, subcommands separate from the main program.
        - Execute callback functions
    '''
    def __init__(self, id: str, argp_args: list, cb: typing.Callable, help='', *args, **kwargs):
        super().__init__(argp_args)
        self.id = id
        self.callback = cb
        self.help = help

    # TODO: Recursive 
    # def format_help(self, msg=''):
        # for arg_def in self.arg_defs:
            # if isinstance(arg_def, Command):
                # # Format commands like this for now:
                # # id        help
                # # TODO: Support sub options in commands
                # # In the future, we want commands like
                # # id        help
                # #   short, long         help
                # #   short, long         help
                # format = ''
                # cmds_msg += format
            # elif isinstance(arg_def, Option):
                # # Default option format:
                # #   -v,  --version              Show program version
                # #   -sb, --sub                  Subscript text
                # space = ' '
                # short = arg_def.short
                # long = arg_def.long
                # help = arg_def.help

                # short_flag = short + ','
                # format = f'{space:<2}{short_flag:<6}{long:<21}{help}\n'
                # options_msg += format
        # pass

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
            self.help = HelpFormatter(arg_defs=args, prog=os.path.basename(sys.argv[0]), usage=usage, desc=desc)

            # Add -h, --help option
            # TODO: Long options are broken
            help_option = Option('-h', '--help', cb=self.help.show_usage, help='Show program usage')
            args.append(help_option)

        super().__init__(args)
        self.argv = sys.argv[1:]
        self.desc = desc

    def parse(self):
        argp_parse(self, self.argv)
