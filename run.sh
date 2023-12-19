#!/bin/bash

if [ ! -d "env" ]; then
    echo "Creating a virtual environment 'env'..."
    python -m venv env
    echo "Virtual environment 'env' created."
else
    echo "Virtual environment 'env' already exists."
fi

if [ ! -d "data" ]; then
    echo "Creating a folder 'data'..."
    mkdir data
    echo "Folder 'data' created."
else
    echo "Folder 'data' already exists."
fi

# Activate the virtual environment
source env/bin/activate

# Install your Python packages from setup.py into the virtual environment
echo "Installing Python packages into the 'env' folder..."
pip install -e .
echo "Python packages installed into the 'env' folder."

# Create an empty device.json file in the data folder
touch data/device.json
