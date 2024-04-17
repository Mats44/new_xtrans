# Library imports
import os
import subprocess
import pkg_resources

# Module imports from local application
from gui import gui

def install_deps():
    # Load already installed packages
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    for package in required_packages:
        package_name = package.split('==')[0]  # Assumption: packages are pinned with ==
        if package_name not in installed_packages:
            subprocess.check_call(['pip', 'install', package])


if __name__ == '__main__':
    
    install_deps() 
    
    # Initialize the GUI
    gui()   