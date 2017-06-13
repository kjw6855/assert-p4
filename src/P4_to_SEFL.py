import json
import sys
import Node
import SEFL_translation

with open(sys.argv[1]) as data_file:    
    program = json.load(data_file)

print SEFL_translation.run(Node.NodeFactory(program))