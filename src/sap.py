from cmapdefs import *
import sys
# import argparse
import re
from flip import flip
from zalgo import zalgo
from morse import to_morse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

MAJOR, MINOR, PATCH = '0', '1', '0'

def convert(char_map, text):
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
    return ''.join([char + strikeover for char in text])

def optmatch(cmd, short, long=''):
    if (long == ''):
        return (cmd == short)
    else:
        return (cmd == short or cmd == long)

# class ArgParser(argparse.ArgumentParser):
    # def error(self, message):
        # sys.stderr.write('error: %s\n' % message)
        # self.print_help()
        # sys.exit()

class CLI():
    def __init__(self, argv, cmds: list):
        self.cmds = cmds

    def find(self):
        res = ''
        for cmd in self.cmds:
            # return(found(self.argv))
            if (cmd.found(self.argv) == 1):
                res = self.short
                break
            elif (cmd.found(self.argv) == 0):
                res = self.long
                break
        return res

class Command():
    def __init__(self, short='', long=''):
        self.short = short
        self.long = long

    def found(self, argv):
        # return True if (short in argv or long in argv) else False
        # if (self.short in argv):
            # return self.short
        # elif (self.long in argv):
            # return self.long
        # else:
            # return ''
        if self.short in argv:
            return 1
        elif self.long in argv:
            return 0
        else:
            return -1


def main():

    # parser = ArgParser(description='Apply string manipulations on text')
    # subparsers = parser.add_subparsers(dest='command', help='[sub-cmd] help')

    # Subcommands
    # subparser = subparsers.add_parser('flip', help='Flips Text')
    # subparser.set_defaults(which='flip')

    # subparser = subparsers.add_parser('zalgo', help='Creates spooky text')
    # subparser.set_defaults(which='zalgo')

    # subparser = subparsers.add_parser('morse', help='Translates text into morse code')
    # subparser.set_defaults(which='morse')

    # parser.add_argument('-v', '--version', action='version', version=f'%(prog)s - v{MAJOR}.{MINOR}.{PATCH}', help='Show program version')
    # parser.add_argument('-V', '--verbose', action='store_true')
    # parser.add_argument('text', metavar='<text>', help='The text input', default=None)
    # parser.add_argument('effects', help='Apply string manipulation', nargs=argparse.REMAINDER, default=None)
    # flipc = Command('flip')

    # cli = CLI(argv, [flipc])

    # for arg in argv:
    # subcmd = sys.argv[0]
    # text = sys.argv[1]

    # args = parser.parse_args()
    # ver = args.verbose
    # text = str(args.text)
    # effects = args.effects
    # subcmd = vars(args)['command']
    arg = sys.argv[1]
    subcmd = arg
    text = sys.argv[2]
    # effects = sys.argv[2:-1]
    # effects = sys.argv[2:-1]
    # effects = [subcmd, sys.argv[2:-1]]
    effects = [subcmd,]
    # effects = sys.argv[3]
    # effects = [arg,]
    # print(arg, text, effects)

    # if cli.find():

    # if not text:
        # sys.exit()

    # Subcommands
    # Add subargs for each of these commands
    # Pass args parameter and parse commands in each function
    if (subcmd == 'flip'):
        flip(text)
    if (subcmd == 'zalgo'):
        zalgo(text)
    if (subcmd == 'morse'):
        print(to_morse(text.upper()))
    # if (subcmd is not None):
        # return

    # Main
    out = ""
    if(len(effects) < 2):
        cmd = effects[0]
        if (optmatch(cmd, '--sub')):
            out = convert(subscriptCharMap, text)
        if (optmatch(cmd, '--super')):
            out = convert(superscriptCharMap, text)
        if (optmatch(cmd, '-ds', '--doublestruck')):
            out = convert(doubleStruckCharMap, text)
        if (optmatch(cmd, '-oe', '--oldeng')):
            out = convert(oldEnglishCharMap, text)
        if (optmatch(cmd, '-med', '--medieval')):
            out = convert(medievalCharMap, text)
        if (optmatch(cmd, '-mono', '--monospace')):
            out = convert(monospaceCharMap, text)
        if (optmatch(cmd, '-b', '--bold')):
            out = convert(boldCharMap, text)
        if (optmatch(cmd, '-i', '--italics')):
            out = convert(italicCharMap, text)
    elif(len(effects) < 3):
        cmd = effects[0]
        opt = effects[1]
        # Handle combinable effects
        if (optmatch(cmd, '-b', '--bold') and optmatch(opt, '-s', '--sans')):
            out = convert(boldSansCharMap, text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-b', '--bold')):
            out = convert(boldItalicCharMap, text)
        if (optmatch(cmd, '-i', '--italics') and optmatch(opt, '-s', '--sans')):
            out = convert(boldItalicSansCharMap, text)
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '-')):
            out = strikethrough(text, u'\u0336')
        if (optmatch(cmd, '-st', '--strike') and optmatch(opt, '~')):
            out = strikethrough(text, u'\u0334')
    print(out)
