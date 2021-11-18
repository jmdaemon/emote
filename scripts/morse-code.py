#!/usr/bin/python

import click

# morse-code.py - Python program to implement Morse Code Translator

MORSE = {
    'A': '.-'        , 'B': '-...'    , 'C': '-.-.'    ,
    'D': '-..'       , 'E': '.'       , 'F': '..-.'    ,
    'G': '--.'       , 'H': '....'    , 'I': '..'      ,
    'J': '.---'      , 'K': '-.-'     , 'L': '.-..'    ,
    'M': '--'        , 'N': '-.'      , 'O': '---'     ,
    'P': '.--.'      , 'Q': '--.-'    , 'R': '.-.'     ,
    'S': '...'       , 'T': '-'       , 'U': '..-'     ,
    'V': '...-'      , 'W': '.--'     , 'X': '-..-'    ,
    'Y': '-.--'      , 'Z': '--..'    , '1': '.----'   ,
    '2': '..---'     , '3': '...--'   , '4': '....-'   ,
    '5': '.....'     , '6': '-....'   , '7': '--...'   ,
    '8': '---..'     , '9': '----.'   , '0': '-----'   ,
    ', ' :'--..--'   , '.': '.-.-.-'  , '?': '..--..'  ,
    '/': '-..-.'     , '-': '-....-'  , '(': '-.--.'   ,
    ')': '-.--.-'
}

def to_morse(msg):
    output = ''
    for char in msg:
        if char != ' ':
            output += MORSE[char] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            output += ' '
    return output

def to_ascii(msg):
    # extra space added at the end to access the
    # last morse code
    msg += ' '
    output = ''
    morse = ''
    for char in msg:
        if (char != ' '):
            i = 0 # keep track of space
            morse += char
        else:
            i += 1              # i == 1 indicates a new character
            if i == 2 :         # i == 2 indicates a new word
                output += ' '   # adding space to separate words
            else:
                # convert morse to ascii
                output += list(MORSE.keys())[list(MORSE.values()).index(morse)]
                morse = ''
    return output

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command  (options_metavar='[options]'        , context_settings=CONTEXT_SETTINGS)
@click.option   ('-V'       , '--version', "version", help='Show program version')
@click.option   ('-v'       , '--verbose', "verbose", help='Show verbose output', default=False)
@click.option   ('-m'       , '--morse', "morse"    , help='Convert ascii to morse code' , is_flag=True, default=False)
@click.option   ('-a'       , '--ascii', "_ascii"   , help='Convert morse code to ascii', is_flag=True, default=False)
@click.argument ('msg'      , metavar="<msg>"       , required=False)
def cli(version, verbose, morse, _ascii, msg):
    if morse:
        print(to_morse(msg.upper()))
    elif _ascii:
        print(to_ascii(msg))
    else:
        print("Show help message")

if __name__ == '__main__':
    cli()
