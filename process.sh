#!/bin/sh

# Run the first Python script
python filter_types.py

# Check if the first script ran successfully
if [ $? -eq 0 ]; then
  echo "filter_types.py completed successfully. Running deduplicate_ontology.py..."
  
  # Run the second Python script
  python deduplicate_ontology.py
  
  # Check if the second script ran successfully
  if [ $? -eq 0 ]; then
    echo "deduplicate_ontology.py completed successfully."
  else
    echo "Error: deduplicate_ontology.py encountered an error."
  fi
else
  echo "Error: filter_types.py encountered an error."
fi
