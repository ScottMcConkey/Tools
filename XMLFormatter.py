#!/usr/bin/env python
"""
XMLFormatter.py: Formats raw XML with nested indentation
"""

__author__ = 'Scott McConkey'
__license__ = 'MIT'

import re
import argparse

# Define patterns (signatures) for xml tag types in one place
OPENSIG = r'<[^\/][!?]*[\w\s\"\'\=\.\-\:\/\+\s*[?]*\s*[^\/]>'
CLOSESIG = r'<\s*\/\s*[\w\s]+>'
CONTSIG = r'<[^\/][\w\s\"\'\=\.\:\-]+\s*[\/]+\s*>'
TEXTSIG = r'[\w\s\"\'\=\.\-\!]+|<!--[\w\s\"\'\=\.\-\!]+-->'

# Define Global Variables
INPUTFILE = str()
OUTPUTFILE = str()
TABULATOR = str()


def parseArgs():
    """Parses the options provided from the command line."""
    parser = argparse.ArgumentParser(description='Outputs formatted XML to file')
    # Add arguments
    parser.add_argument('-if', '--inFile', type=str,
                        help='Name of File containing the XML to be parsed. E.G. \'-if="MySource.xml"\'', required=True)
    parser.add_argument('-of', '--outFile', type=str,
                        help='Name of File to which results will be output. E.G. \'-of="Output.xml"\'', required=True)
    parser.add_argument('-t', '--tabStyle', type=str,
                        help='Tab Delimiter. E.G. \'-t="\t"\'. Default is two spaces.', required=False, default='  ')
    args = parser.parse_args()
    setGlobals(args)

def setGlobals(argobj):
    global INPUTFILE
    INPUTFILE = argobj.inFile
    global OUTPUTFILE
    OUTPUTFILE = argobj.outFile
    global TABULATOR
    TABULATOR = argobj.tabStyle


class XMLTag:
    """Takes an XML element and determines previous, current, and next tag types."""
    previousType = ''
    currentType = ''
    nextType = ''

    def __init__(self, itemindex, list):
        # Set Previous Type
        if itemindex != 0:
            if re.match(OPENSIG, list[itemindex-1]):
                self.previousType = 'open'
            elif re.match(CLOSESIG, list[itemindex-1]):
                self.previousType = 'close'
            elif re.match(CONTSIG, list[itemindex-1]):
                self.previousType = 'contained'
            elif re.match(TEXTSIG, list[itemindex-1]):
                self.previousType = 'text'
        else:
            self.previousType = 'none'
        # Set Current Type
        if re.match(OPENSIG, list[itemindex]):
            self.currentType = 'open'
        elif re.match(CLOSESIG, list[itemindex]):
            self.currentType = 'close'
        elif re.match(CONTSIG, list[itemindex]):
            self.currentType = 'contained'
        elif re.match(TEXTSIG, list[itemindex]):
            self.currentType = 'text'
        # Set Next Type
        if itemindex != (len(list)-1):
            if re.match(OPENSIG, list[itemindex+1]):
                self.nextType = 'open'
            elif re.match(CLOSESIG, list[itemindex+1]):
                self.nextType = 'close'
            elif re.match(CONTSIG, list[itemindex+1]):
                self.nextType = 'contained'
            elif re.match(TEXTSIG, list[itemindex+1]):
                self.nextType = 'text'
        else:
            self.nextType = 'none'

def applyFormatting(list):
    """Takes list input and uses to created nested output."""
    output = ''
    nestLevel = 0
    for tag in range(len(list)):
        item = XMLTag(tag, list)
        # Is Opening Tag
        if item.currentType == 'open':
            # Consider Previous
            if item.previousType == 'none':
                output += list[tag]
            elif item.previousType == 'open':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'close':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'contained':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'text':
                output += (TABULATOR * nestLevel) + list[tag]
            # Consider Next
            if item.nextType == 'open':
                output += '\n'
                nestLevel += 1
            elif item.nextType == 'close':
                pass
            elif item.nextType == 'contained':
                output += '\n'
                nestLevel += 1
            elif item.nextType == 'text':
                pass
        # Is Closing Tag
        elif item.currentType == 'close':
            # Consider Previous
            if item.previousType == 'none':
                output += list[tag]  # this should not happen, but handle it anyway
            elif item.previousType == 'open':
                output += list[tag]
            elif item.previousType == 'close':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'contained':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'text':
                output += list[tag]
            # Consider Next
            if item.nextType == 'open':
                output += '\n'
            elif item.nextType == 'close':
                output += '\n'
                nestLevel -= 1
            elif item.nextType == 'contained':
                output += '\n'
            elif item.nextType == 'text':
                output += '\n'
        # Is Contained
        elif item.currentType == 'contained':
            # Consider Previous
            if item.previousType == 'none':
                output += list[tag]  # this should not happen, but handle it anyway
            elif item.previousType == 'open':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'close':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'contained':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'text':
                output += (TABULATOR * nestLevel) + list[tag]
            # Consider Next
            if item.nextType == 'open':
                output += '\n'
            elif item.nextType == 'close':
                output += '\n'
                nestLevel -= 1
            elif item.nextType == 'contained':
                output += '\n'
            elif item.nextType == 'text':
                output += '\n'
        # Is Text
        elif item.currentType == 'text':
            # Consider Previous
            if item.previousType == 'none':
                output += list[tag]  # this should not happen, but handle it anyway
            elif item.previousType == 'open':
                output += list[tag]
            elif item.previousType == 'close':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'contained':
                output += (TABULATOR * nestLevel) + list[tag]
            elif item.previousType == 'text':
                output += list[tag]  # this should not happen, but handle it anyway
            # Consider Next
            if item.nextType == 'open':
                output += '\n'
            elif item.nextType == 'close':
                pass
            elif item.nextType == 'contained':
                output += '\n'
            elif item.nextType == 'text':
                pass
    return output


def main():
    returntext = str()

    # Get the arguments
    parseArgs()

    # Read from Input File
    try:
        if INPUTFILE is not None:
            i = ''
            with open(INPUTFILE, 'r') as infile:
                i = infile.read()
                returntext = i.replace('\n', '')
    except:
       print("Error: Read failed on input file. Are you sure the file name was spelled correctly?")

    # Split into tags and text
    breakdown = (re.findall(OPENSIG + '|' + CONTSIG + '|' + CLOSESIG + '|' + TEXTSIG, returntext))
    # Filter out whitespace
    breakdown = [x for x in breakdown if not re.match(r'\s+', x)]
    # Apply Formatting
    returntext = applyFormatting(breakdown)

    # Write to Output File
    try:
        if OUTPUTFILE is not None:
            o = open(OUTPUTFILE,'w+')
            o.write(returntext)
    except:
        print("Error: Write failed on output file. Do you have write access in this directory?")


if __name__ == "__main__":
    main()