import json


# Function to load the ontology from a JSON file
def load_ontology(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Helper function to count descendants
def count_descendants(ontology):
    if isinstance(ontology, dict):
        # If it's a dictionary, count each child plus the child's descendants
        return 1 + sum(count_descendants(v) for v in ontology.values())
    elif isinstance(ontology, list):
        # If it's a list, count each item plus the item's descendants
        return len(ontology) + sum(count_descendants(v) for v in ontology)
    else:
        # Leaf node, no descendants
        return 0


# Function to filter self-referential keys
def filter_self_referential(ontology, parent_key=None):
    if isinstance(ontology, dict):
        keys_to_delete = []
        for key, value in ontology.items():
            if key == parent_key:
                keys_to_delete.append(key)
            else:
                ontology[key] = filter_self_referential(value, key)
        for key in keys_to_delete:
            del ontology[key]
    elif isinstance(ontology, list):
        for i, item in enumerate(ontology):
            ontology[i] = filter_self_referential(item, parent_key)
    return ontology


# Function to find duplicates recursively
def find_duplicates(ontology, path="", duplicate_keys=None, paths_dict=None):
    if duplicate_keys is None:
        duplicate_keys = set()
    if paths_dict is None:
        paths_dict = {}

    if isinstance(ontology, dict):
        for key, value in ontology.items():
            new_path = f"{path}/{key}" if path else key
            if key in paths_dict:
                duplicate_keys.add(key)
                paths_dict[key].append(new_path)
            else:
                paths_dict[key] = [new_path]
            find_duplicates(value, new_path, duplicate_keys, paths_dict)

    elif isinstance(ontology, list):
        for index, item in enumerate(ontology):
            new_path = f"{path}/{index}"
            find_duplicates(item, new_path, duplicate_keys, paths_dict)

    return duplicate_keys, paths_dict


# Function to ask the user which duplicate key path to keep
def ask_user_for_selection(duplicate_key, paths, ontology):
    print(f"\nDuplicate key found: '{duplicate_key}'")
    # Automatically select the path if there is only one option
    if len(paths) == 1:
        print(
            f"Only one path exists for '{duplicate_key}', automatically selected: {paths[0]}"
        )
        return 0  # Automatically return the index of the single path

    print("Please choose which path to keep by entering the number:")
    print(f"0: Keep all paths for '{duplicate_key}'")
    for i, path in enumerate(paths, start=1):
        # Adjust the descendant count by subtracting 1 to not count the current node
        descendant_count = count_descendants(retrieve_subtree(ontology, path)) - 1
        print(f"{i}: {path} (descendants: {descendant_count})")
    selected = int(input("Enter your choice: ")) - 1
    return selected


# Function to retrieve a subtree from the ontology given a path
def retrieve_subtree(ontology, path):
    keys = path.strip("/").split("/")
    subtree = ontology
    for key in keys:
        if isinstance(subtree, list) and key.isdigit():
            subtree = subtree[int(key)]
        elif isinstance(subtree, dict) and key in subtree:
            subtree = subtree[key]
        else:
            # If the path is incorrect or the data is not as expected, report it
            print(f"Error retrieving subtree: path '{path}' is not valid.")
            return {}
    return subtree


# Function to update the paths_dict after a deletion
def update_paths_dict(paths_dict, selected_path, deleted_paths):
    # Remove invalid paths
    for key, paths in list(paths_dict.items()):
        paths_dict[key] = [
            path
            for path in paths
            if path not in deleted_paths and not path.startswith(selected_path)
        ]
        if not paths_dict[key]:
            del paths_dict[key]


# Function to remove non-selected duplicate paths from the ontology
def remove_non_selected_paths(ontology, paths_dict, duplicate_key, selected_index):
    if selected_index == -1:
        # If the user selects to keep all paths, do nothing
        return ontology, paths_dict
    
    # Copy of the ontology for safe modifications
    modified_ontology = json.loads(json.dumps(ontology))

    # Get the selected path
    selected_path = paths_dict[duplicate_key][selected_index]

    # Remove all other paths
    for path in paths_dict[duplicate_key]:
        if path != selected_path:
            delete_path(modified_ontology, path)

    # Update paths_dict after deletions
    paths_dict = rebuild_paths_dict(modified_ontology)

    return modified_ontology, paths_dict


# Function to rebuild paths_dict after deletion
def rebuild_paths_dict(ontology):
    new_paths_dict = {}
    find_duplicates(ontology, duplicate_keys=set(), paths_dict=new_paths_dict)
    return new_paths_dict


# Function to delete the specified path from the ontology
def delete_path(ontology, path):
    keys = path.strip("/").split("/")
    current = ontology
    for key in keys[:-1]:
        if key.isdigit():
            current = current[int(key)]
        else:
            current = current[key]

    last_key = keys[-1]
    if last_key.isdigit():
        del current[int(last_key)]
        return True
    else:
        if last_key in current:
            del current[last_key]
            return True
    return False


# Main function to orchestrate the deduplication process
def deduplicate_ontology(file_path):
    ontology = load_ontology(file_path)
    print("Loaded ontology from file...")

    # Filter self-referential keys
    ontology = filter_self_referential(ontology)
    print("Filtered self-referential keys...")

    duplicate_keys, paths_dict = find_duplicates(ontology)
    print("Found duplicate keys...")
    print(f"Number of duplicate keys: {len(duplicate_keys)}")

    # Sort by the minimum path length of all paths for each key
    for duplicate_key in sorted(
        duplicate_keys, key=lambda k: min(len(path) for path in paths_dict[k])
    ):
        paths = paths_dict[duplicate_key]
        selected_index = ask_user_for_selection(duplicate_key, paths, ontology)
        ontology, paths_dict = remove_non_selected_paths(
            ontology, paths_dict, duplicate_key, selected_index
        )

    return ontology


# Specify the path to your ontology JSON file
file_path = "filtered_working_ontology.json"

print("Deduplicating ontology...")
# tmp = input("Press enter to continue...")
# print(tmp)
# Run the deduplication process
modified_ontology = deduplicate_ontology(file_path)

# Save the modified ontology to a new JSON file
output_file_path = "processed_working_ontology.json"
with open(output_file_path, "w") as file:
    json.dump(modified_ontology, file, indent=2)

# Print how big the new ontology is
print(f"Ontology size after duplicate removal: {count_descendants(modified_ontology)}")
