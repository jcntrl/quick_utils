#!/bin/bash

# Check if at least one argument (directory) is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <archive_name> <directory1> [directory2] ..."
    exit 1
fi

# The first argument is the archive name
archive_name=$1
shift  # Shift to get the rest of the arguments (the directories)

# Compress directories into a tar.gz archive using pigz
tar cf - "$@" | pigz -9 -p 8 > "${archive_name}.tar.gz"

echo "Compression complete: ${archive_name}.tar.gz"
