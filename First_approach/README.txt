I send the following prompt along with my processed_working_ontology.json file in advancaed data analysis mode to chat gpt-4:

____________________________________________________________


I would like help constructing a fine grained ontology of types. I have constructed a seed ontology that I will provide to you which contains some 140 or so types placed in a JSON structure. They outline the rough hierarchy that I would like you to respect when adding new terms to the ontology. Each term should only exist once in the ontology, and it should be hierarchical with children representing is-a relationships with their parents in the tree. I am going to provide you with types iteratively to add to the tree, and I would like you to place them wherever they are appropriate in the tree, potentially adding new branches when it is necessary to accurately place a new term. Respect the term wording as I provide it exactly. Use your language knowledge to place the terms, not a rule based approach. Here is the initial seed ontology to start from and add to. 

__________________________________________________________________________

with the custom instructions boxes set to blank for the "What would you like ChatGPT to know about you to provide better responses?", and for the
 "How would you like ChatGPT to respond? I have the following:
 ____________________________________________________________

We are trying to build a fine grained entity types taxonomy. The goal is to create a useful taxonomy with a balance of both breadth and depth for the created categories. Output as JSON when possible. Do not create any new types, only use the ones provided to build the taxonomy tree. The resulting ontology should be useful for a wide range of scenarios.


 __________________________________________________________

Then after its response send batches of 10-40 terms at a time (unsure if more will break yet) from types_left_to_add.text
Either after each batch or after every few batches you can grab the output json if it gives it, or prompt it to output the whole ontology so far
This will give a json file to input into working_ontology.js (might have to replace single quote '  with double quote " but it is simple replace all)
Then run the process script (chmod +x process.sh) which runs the two filtering scripts individually
See those two scripts for their details, but broadly the first script, filter_types.py reads in the current working ontology and filters out any types that are not from the ultrafine 10,331 types set
Then it creates a new file of the types left to add to the ontology (removed those already in json)

Next the second script, deduplicate_ontology.py first removes any instances of a word being set as a child of itself, which can occasionally occur if it runs into errors due to its environment of running inside an ipynb environment
Sometimes code partially executes and then errors, so it tries again, but it doesn't clean up the sideeffects of the previous attempt (like adding a key to somewhere else)

Then the script finds all instances of duplicate keys, which again can occur from the same error as mentioned. Sometimes these errors are not immediately caught and other entities are placed as children of this duplicate
This script finds each duplicate and prompts you to select which path to keep (with their number of children of each of the paths), and the other(s) are deleted

This ensures that only 1 instance of each key is present in the final processed ontology json file. 

The goal of this process is to allow you to iteratively add some number of types to the ontology, then gets its internal json representation, 
and filter it into a new set of types_left_to_add.txt and processed_working_ontology.json which could then be reinput or used to start a new session in the future.
This process also allows th results to be checkpointed and potentially rolled back