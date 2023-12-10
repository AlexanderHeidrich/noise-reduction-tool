#!/bin/bash

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
else
    echo "Error: Python 3 is not installed. Please install Python 3 and run this script again."
    exit 1
fi

# Install other OS dependencies
brew install mediainfo

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

echo "Setup complete. Activate the virtual environment using 'source venv/bin/activate'."
