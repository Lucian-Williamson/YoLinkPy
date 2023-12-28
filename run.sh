User
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

# Create config.yaml file if it doesn't exist
if [ ! -f "config.yaml" ]; then
    echo "Creating config.yaml file..."
    cat <<EOF >config.yaml
load_local: true
homes: []
EOF
    echo "config.yaml file created."
else
    echo "config.yaml file already exists."
fi

# Activate the virtual environment
source env/bin/activate

# Install your Python packages from setup.py into the virtual environment
echo "Installing Python packages into the 'env' folder..."
pip install -e .
echo "Python packages installed into the 'env' folder."

