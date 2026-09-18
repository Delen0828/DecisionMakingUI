#!/bin/bash

# Define the directory where the images are located
dir="img"

# Move to the target directory
cd "$dir" || exit

# Get a list of all .png files
files=( *.png )

# Loop through the files and rename them sequentially
counter=1
for file in "${files[@]}"; do
    mv "$file" "$counter.png"
    ((counter++))
done

echo "Renaming completed!"