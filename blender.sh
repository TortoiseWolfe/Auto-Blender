#!/bin/bash
# Auto-Blender: WSL2 -> Windows Blender wrapper
# Usage: ./blender.sh scripts/create_scrum_level1.py

BLENDER="/mnt/c/Program Files/Blender Foundation/Blender 5.0/blender.exe"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if Blender exists
if [ ! -f "$BLENDER" ]; then
    echo "Error: Blender not found at: $BLENDER"
    echo "Please update the BLENDER path in this script."
    exit 1
fi

# Check for script argument
if [ -z "$1" ]; then
    echo "Usage: ./blender.sh <script.py>"
    echo "Example: ./blender.sh scripts/create_scrum_level1.py"
    exit 1
fi

# Get absolute path to the Python script
SCRIPT_PATH="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"

# Convert WSL path to Windows path for the script
WIN_SCRIPT_PATH=$(wslpath -w "$SCRIPT_PATH")

echo "Running Blender with script: $WIN_SCRIPT_PATH"
echo "Output will be in: $SCRIPT_DIR"

# Run Blender in background mode with the Python script
"$BLENDER" --background --python "$WIN_SCRIPT_PATH"
