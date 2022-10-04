from loguru import logger
import typing, sys
# Reasons why I don't like argparse
# usage and other names aren't capitalized.
# cannot accept '-' or '--' as arguments 
# only one operation/subcommand can be processed at a time

# Reasons why I don't like custom parsing
# no help/usage string
# awkward inputs and input handling
# lack of code reuse between projects

# Argp
class Option():
    def __init__(self, short: str, long: str, val='', flag=False, id='', help=''):
        self.id = id
        self.short = short
        self.long = long
        self.flag = flag
        self.val = val
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
                    # TODO: Recursively parse the damn thing
                    arg.parse(argv[index:])
            elif isinstance(arg, Option):
                logger.debug('Is Option')
                self.arg_vals[arg.id] = True if arg.is_flag() else arg
            else:
                # Assume we are only left with an argument
                logger.debug('Is Argument')
                self.arguments.append(argv)
            index += 1

class Command(ArgParser):
    # Commands
    # Should be able to:
        # - Specify their own arguments, options, further subcommands
        # - Specify and execute custom callback with their specified options
        # - Embed themselves in other commands
    def __init__(self, id: str, argp_args: list, callback: typing.Callable, help='', *args, **kwargs):
        super().__init__(argp_args)
        self.id = id
        self.callback = callback
        self.help = help

class Argp(ArgParser):
    def __init__(self, args: list, description=''):
        super().__init__(args)
        self.argv = sys.argv[1:]
        self.description = description

    def parse(self):
        super().parse(self.argv)

