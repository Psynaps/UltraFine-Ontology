# Program that reads in a file ontology.json line by line and outputs a file processed_ontology.json
# which has hadd all lines which start with // removed.
#

import json
import sys


def removeComments(ontology):
    with open(ontology) as f:
        # Read line by line and remove comments
        lines = f.readlines()
    with open("processed_ontology.json", "w") as file:
        for line in lines:
            if not line.strip().startswith("//"):
                # remove line if it starts with //
                print(line)
                # write to new file
                file.write(line)


removeComments("ontology.json")
