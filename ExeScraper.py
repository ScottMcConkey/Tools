#!/usr/bin/env python
"""Finds all EXE files in the current directory and
    determines whether they are 32 or 64 bit.
    Designed for Python 3.5"""

__author___ = 'Scott McConkey'
__license__ = 'MIT'

import struct
import os
import re

def GetExeBitSize(executable):
    '''Calculates whether a given executable file is 32 or 64 bit
    based on header data'''
    # ref http://stackoverflow.com/questions/1345632/determine-if-
    # an-executable-or-library-is-32-or-64-bits-on-windows
    # Known architecture signatures
    IMAGE_FILE_MACHINE_I386=332
    IMAGE_FILE_MACHINE_IA64=512
    IMAGE_FILE_MACHINE_AMD64=34404
    f=open(executable, 'rb')
    # .decode required for Python 3
    s=f.read(2).decode(encoding="utf-8", errors="strict")

    if s != "MZ":
        bitSize = "Not an EXE file"
    else:
        f.seek(60)
        s=f.read(4)
        header_offset=struct.unpack("<L", s)[0]
        f.seek(header_offset+4)
        s=f.read(2)
        machine=struct.unpack("<H", s)[0]
        # Compare header data to known architecture signatures
        if machine==IMAGE_FILE_MACHINE_I386:
            bitSize = "32-bit"
        elif machine==IMAGE_FILE_MACHINE_IA64:
            bitSize = "64-bit"
        elif machine==IMAGE_FILE_MACHINE_AMD64:
            bitSize = "64-bit"
        else:
            bitSize = "Unknown architecture"
    f.close()
    return bitSize


def main():
    print("***********************************************************")
    print("* ExeScraper.py")
    print("* Finds all EXE files in the current directory and ")
    print("* determines whether they are 32 or 64 bit")
    print("***********************************************************")
    print("\r\r")

    # get a list of directory files
    f = os.listdir('.')

    # setup the display grid
    template = "{0:30}{1:8}"

    # get only exe files, and not ones with .bak or .manifest or anything like that
    hasValue = True
    for file in f:
        if re.search(r'^\w+\.exe$', file):
            hasValue = True
            print("-----------------------------------------------------------")
            print(template.format(file, GetExeBitSize(file)))
    if not hasValue:
        print("There are no EXE files in this folder.")
    else:
        print("-----------------------------------------------------------")

    print("\n")

    # hang the console so user can see the output
    input("press enter to exit")

if __name__ == '__main__':
    main()
