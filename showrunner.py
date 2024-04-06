# Library imports
import os
import subprocess

# Module imports from local application
from gui import gui

def install_deps(): # Install dependencies from requirements.txt
    with open('requirements.txt', 'r') as f:
        packages = f.read().splitlines()

    for package in packages:
        subprocess.check_call(['pip', 'install', package])


if __name__ == '__main__':
    
    install_deps() 
    
    # Initialize the GUI
    gui()   