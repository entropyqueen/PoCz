#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <quentrg@gmail.com> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# Quentin Roland-Gosselin (@Ark_444)
# Github: https://github.com/Ark444
# ----------------------------------------------------------------------------

# This tool is just another simple script that applies the ROT encoding
# with a bunch of (I hope) useful options
# Hope you'll enjoy even if it's still really simple =)

import sys
import argparse
import string
import os

CHUNK_SIZE = 65536

class Shifter(object) :

    def __init__(self, shift, input_file = None, output_file = None,
                 bf=False, alpha=True, incremental='', decremental='',
                 increment_val=1, decrement_val=1):
        """
        initializes a Shifter
        """
        self._shift = int(shift) if shift != None else None
        self._infile = input_file
        self._outfile = output_file
        self._bf = bf
        self._alpha = alpha
        if self._infile != None:
            try:
                self._in = open(self._infile, "rb")
            except IOError(e):
                raise(e)
        else:
            self._in = sys.stdin

        if self._outfile != None:
            try:
                self._out = open(self._outfile, "wb")
            except IOError(e):
                raise(e)
        else:
            self._out = sys.stdout

        self._inc = os.fsencode(incremental if incremental != None else '')
        self._dec = os.fsencode(decremental if decremental != None else '')
        self._inc_v = int(increment_val, 0) if increment_val != None else 1
        self._dec_v = int(decrement_val, 0) if decrement_val != None else 1
            
    def clean(self):
        """
        Closes all used files.
        """
        if self._infile != None:
            self._in.close()
        if self._outfile != None:
            self._out.close()

    # shifting process
    def _process(self, shift):
        """
        background function for process
        should not be use directly
        """
        try:
            self._in.seek(0)
        except:
            pass
        for chunk in iter(lambda: self._in.read(CHUNK_SIZE), ''):
            chunk = os.fsencode(chunk)
            if chunk == b'':
                break;
            buff = b''
            if self._alpha == True:
                for x in chunk:
                    if os.fsencode(chr(x)) in self._inc:
                        self._shift += self._inc_v
                        shift = self._shift
                    if x in self._dec:
                        self._shift -= self._dec_v
                        shift = self._shift
                    if x in os.fsencode(string.ascii_lowercase):
                        buff += os.fsencode(chr((x - ord('a') + shift) % 26 + ord('a')))
                    elif x in os.fsencode(string.ascii_uppercase):
                        buff += os.fsencode(chr((x - ord('A') + shift) % 26 + ord('A')))
                    else :
                        buff += os.fsencode(chr(x))
            else:
                buff = b''.join([os.fsencode(chr((x + shift) % 255)) for x in chunk])

            # unfortunatly we cannot write bytes directly to stdout
            # TODO: maybe find another prettier way to do that
            if self._outfile != None:
                self._out.write(buff)
            else:
                self._out.write(os.fsdecode(buff))

    def process(self):
        """
        runs the shifting process, using the parameters given in the constructor
        """
        if self._bf == True:
            if self._alpha == True:
                bf_maxval = 26
            else:
                bf_maxval = 255
            for x in range(bf_maxval):
                if self._outfile != None:
                    self._out.write(os.fsencode('\nRound {} out of {}:\n'.format(x, bf_maxval)))
                else:
                    self._out.write('\nRound {} out of {}:\n'.format(x, bf_maxval))
                self._process(x)
        else:
            self._process(self._shift)
            

if __name__ == "__main__":

    if len(sys.argv) == 1:
        # if no args at all, let's just do a rot13
        Shifter(13).process()
        exit()
    
    parser = argparse.ArgumentParser(description='Rotates char in string or files')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--value', '-v', metavar='X',
                        help='value for the rotation')
    group.add_argument('--bruteforce', '-b', action='store_true',
                        help='do not specify value, try them all')
    parser.add_argument('--alphabetical', '-a', action='store_true',
                        help='rotation will occur only on alpahbetical char')
    parser.add_argument('--file', '-f', metavar='FILE',
                        help='input file to read from')
    parser.add_argument('--output', '-o', metavar='FILE',
                        help='output file to store the result')
    parser.add_argument('--incremental', '-i', metavar='STR',
                        help='increments the value X when char of STR is found')
    parser.add_argument('--decremental', '-d', metavar='STR',
                        help='decrements the value X when a char of STR is found')
    parser.add_argument('--increment-value', metavar='NB',
                        help='give a specific value NB when applying increments')
    parser.add_argument('--decrement-value', metavar='NB',
                        help='give a specific value NB when applying decrements')
    args = parser.parse_args()

    shifter = Shifter(
        args.value,
        args.file,
        args.output,
        args.bruteforce,
        args.alphabetical,
        args.incremental,
        args.decremental,
        args.increment_value,
        args.decrement_value
    )
    shifter.process()
    shifter.clean()
