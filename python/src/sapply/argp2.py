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

        self.set_id_from_long()

    def set_id_from_long(self):
        ''' Sets the option id from the long option specifier '''
        if self.long[0:1] == '--':
            self.id = self.long[1:]

    def is_flag(self):
        return True if self.flag else False

class ArgParser():
    def __init__(self, argp_args: list, help='', *args, **kwargs):
        self.args = argp_args
        self.help = help

        # Initialize the keywords for easy matching
        self.keynames: dict = {}
        for arg in self.args:
            if isinstance(arg, Command):
                self.keynames[arg.invoke] = arg
            # TODO: Create option mapping where short, long options could match id
            elif isinstance(arg, Option):
                # self.keynames[arg.id] = arg
                self.keynames[arg.id] = arg

        # Stores the values of the options & arguments
        self.keyvalues: dict = {}
        self.arguments = []

    def is_option(self, option):
        for argid, arg in self.keynames.items():
            # logger.debug(f'argid: {argid}')
            # logger.debug(f'arg: {arg}')
            # opt: Command | Option = self.keyvalues[argid]
            opt: Command | Option = self.keynames[option]
            # logger.debug(f'opt: {opt}')
            if isinstance(opt, Option):
                if arg.long == option:
                    return True
                elif arg.short == option:
                    return True
        return False

    def is_cmd(self, invoke):
        for argid, arg in self.keynames.items():
            # logger.debug(f'argid: {argid}')
            # logger.debug(f'arg: {arg}')
            # cmd: Command | Option = self.keyvalues[argid]
            # logger.debug(f'cmd: {cmd}')
            cmd: Command | Option = self.keynames[invoke]
            if isinstance(cmd, Command):
                if arg.invoke == invoke:
                    return True
        return False

    def parse(self, argvs: list):
        index = 1
        logger.info('Parsing arguments')

        for argv in argvs:
            logger.debug(f'Current Argument: {argv}')

            if self.is_option(argv) or self.is_cmd(argv):
                arg: Command | Option = self.keynames[argv]
                logger.debug(f'arg: {arg}')

                if isinstance(arg, Command):
                    logger.info('Argument is Command')
                    if arg.callback != None:
                        arg.callback()
                    else:
                        arg.parse(argv[index:])
                    continue

                elif isinstance(arg, Option):
                    logger.info('Argument is Option')
                    # Set the value of the option if any
                    # If option == flag, toggle flag value
                    # Set option in main 
                    if arg.is_flag():
                        self.keyvalues[arg.id] = True
                    else:
                         self.keyvalues[arg.id] = [arg.short, arg.long, arg.val]
                    continue
            else:
                # Assume we are only left with an argument
                logger.info('Argument is an Argument')
                self.arguments.append(argv)
            index += 1

        logger.debug(f'argp.keyvalues: {self.keyvalues}')

class Command(ArgParser):
    # Commands
    # Should be able to:
        # - Specify their own arguments, options, further subcommands
        # - Specify and execute custom callback with their specified options
        # - Embed themselves in other commands
    def __init__(self, invoke: str, argp_args: list, callback: typing.Callable, help='', *args, **kwargs):
        super().__init__(argp_args)
        self.invoke = invoke
        self.callback = callback
        self.help = help

class Argp(ArgParser):
    def __init__(self, args: list, description=''):
        super().__init__(args)
        self.argv = sys.argv[1:]
        self.description = description

    def parse(self):
        super().parse(self.argv)

