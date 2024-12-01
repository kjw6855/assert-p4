#!/usr/bin/env python3

import json
import sys
import Node
import C_translation
import parse_forwarding_rules

from os.path import splitext, basename
from optparse import OptionParser
import argparse
import argcomplete
from argcomplete.completers import FilesCompleter

def main(args):
    with open(args.p4_json) as data_file:
        program = json.load(data_file)

    if args.commands != None:
        forwardingRules = parse_forwarding_rules.parse(args.commands)
        #print(forwardingRules)
    else:
        forwardingRules = None

    model = C_translation.run(Node.NodeFactory(program), forwardingRules, args)
    model = C_translation.post_processing(model)

    #Print output to file
    if not args.outfile:
        p4_program_name = splitext(basename(args.p4_json))[0]
        assert_p4_outfile = "{}.{}".format(p4_program_name,
                'cpp' if args.genCpp else 'c')
    else:
        assert_p4_outfile = args.outfile

    with open(assert_p4_outfile, "w") as output:
        output.write(model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fuzzer", dest="libfuzzerMode",
            help="enable libfuzzer mode", action="store_true", default=False)
    parser.add_argument("-i", "--input", dest="p4_json", metavar="FILE", type=str,
            help="input p4 IR json file").completer = FilesCompleter()
    parser.add_argument("-o", "--output", dest="outfile", metavar="FILE", type=str,
            help="specify output file name").completer = FilesCompleter()
    parser.add_argument("-c", "--commands", dest="commands", metavar="FILE", type=str,
            help="add file for control plane rules").completer = FilesCompleter()
    parser.add_argument("--cpp", dest="genCpp",
            help="enable .cpp mode", action="store_true", default=False)
    parser.add_argument("--verbose", dest="verbose",
            action="store_true", default=False)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if not args.p4_json:
        parser.error("missing input P4-IR json file")

    if args.libfuzzerMode : args.genCpp = True

    main(args)
