import json


def check_type_in_ontology(ontology, target_type):
    for key, value in ontology.items():
        if key == target_type:
            return True
        if isinstance(value, dict):
            if check_type_in_ontology(value, target_type):
                return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    if check_type_in_ontology(item, target_type):
                        return True
    return False


def check_type_in_file(ontology, types_set, not_in_file):
    for key, value in ontology.items():
        if key not in types_set:
            not_in_file.append(key)
        if isinstance(value, dict):
            check_type_in_file(value, types_set, not_in_file)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    check_type_in_file(item, types_set, not_in_file)


def prune_ontology(ontology, not_in_file):
    keys_to_delete = []
    for key, value in ontology.items():
        if key in not_in_file:
            keys_to_delete.append(key)
        if isinstance(value, dict):
            prune_ontology(value, not_in_file)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    prune_ontology(item, not_in_file)
    for key in keys_to_delete:
        del ontology[key]


# Read in the ontology
with open("working_ontology.json", "r") as f:
    ontology = json.load(f)

# Read in the types
types = []
with open("ordered-types.txt", "r") as f:
    for line in f:
        types.append(line.strip())

types_set = set(types)

# Filter the types that are not in the ontology
filtered_types = [t for t in types if not check_type_in_ontology(ontology, t)]

# Write the filtered types to a file
with open("types_left_to_add.txt", "w") as f:
    for t in filtered_types:
        f.write(t + "\n")

# Check for types in ontology but not in file
not_in_file = []
check_type_in_file(ontology, types_set, not_in_file)
print(
    f"{len(not_in_file)} types in ontology but not in file. Removing them from ontology"
)

# Prune the ontology
prune_ontology(ontology, not_in_file)

# Outputs a new ontology file with any hallucinated types removed
with open("filtered_working_ontology.json", "w") as f:
    json.dump(ontology, f, indent=4)

print(f"Filtered {len(filtered_types)} types.")
print("Filtered types written to types_left_to_add.txt")
print(f"Pruned ontology written to filtered_working_ontology.json")

# Then you are able to use filtered_working_ontology.json as a new seed ontology,
# and the types_left_to_add.txt as a new list of types to add, to further prompt to add new terms

# TODO: add duplicate type checking and filtering of those types
