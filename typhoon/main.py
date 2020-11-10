#!/usr/bin/env python

import sys
import argparse
import marshal
import time
import random
import struct
import py_compile

from .obfuscate import Obfuscate


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--input', '-i',
        type=argparse.FileType('r'), default=sys.stdin,
        help = 'Python file to obfuscate')

    argparser.add_argument('--output', '-o',
        type=argparse.FileType('wb'), default=sys.stdout,
        help = 'Python file to obfuscate')

    argparser.add_argument('--key', '-k',
        required=True,
        help='Encoder key')

    argparser.add_argument('--debug', '-d',
        action='store_true',
        help='Print verbose debugging information')

    args = argparser.parse_args()

    program = args.input.read()

    code = Obfuscate.Obfuscate(program, key=args.key, debug=args.debug)

    t = int(time.time()) - (random.randrange(90,1000) * 86400)
    args.output.write(py_compile.MAGIC)
    args.output.write(struct.pack('<I', t))
    marshal.dump(code, args.output)
    args.output.close()


if '__main__' == __name__:
    main()
