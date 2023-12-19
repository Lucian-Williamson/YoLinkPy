@echo off

IF NOT EXIST env (
    echo Creating a virtual environment 'env'...
    python -m venv env
    echo Virtual environment 'env' created.
) ELSE (
    echo Virtual environment 'env' already exists.
)

IF NOT EXIST data\ (
    echo Creating a folder 'data'...
    mkdir data
    echo Folder 'data' created.
) ELSE (
    echo Folder 'data' already exists.
)

REM Activate the virtual environment
call env\Scripts\activate

REM Install your Python packages from setup.py into the virtual environment
echo Installing Python packages into the 'env' folder...
pip install -e .
echo Python packages installed into the 'env' folder

REM Create an empty device.json file in the data folder
type nul > data\device.json
