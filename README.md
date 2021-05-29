# System Setup
This Python tool will automatically install system dependencies by executing shell commands found in a json file. The json file it reads from is organized into packages. The installer will remember what packages have been installed and not try to install a completed package twice. The installer also has an option to only install a specific package.

The installer will also let you know which command and which packages have failed, and can break and wait for user processes to complete.

It is recommended you use python3 to run this project.

## How to run installer
Run the python file installer.py ex: 'python3 installer.py'

## Installer dependencies
The installer requires a nonstandard python package called json5, which can be installed with the following command (requires python3 and pip): 'pip3 install json5'

To clone, install dependencies, and run the script in one command, run:
'sudo apt-get update && sudo apt-get install -y python3 python3-pip git && pip3 install json5 && git clone https://github.com/dolphonie/system-setup.git && cd system-setup && python3 installer.py'

## Available command-line arguments
- --package: allows for installation of multiple specified package from list, after which program will terminate. Needs to be followed by list of packages in json file separated by a space
- --workdir: by default the program creates a directory in ~/temp and creates all intermediate files in that directory. This argument lets you provide a filepath for these temp files to be created in instead
- --ignore-progress: ordinarily, the same package can't be installed twice. This argument ignores the progress files and installs all packages from the beginning
- --file: by default the program gets commands from a file called packages.json5. This flag lets you specify which JSON file you'd like the program to pull from

## JSON file format
The json file containing all lines to be executed must be grouped in the following way: (Note, the program supports json5 file formatting, allowing for commments and trailing commas)

- Outmost structure needs to be dictionary with key string, item list
- Each entry in the dictionary should refer to a package and the key should be the package name
- Each line of the program to be run should be an item in this dictionary, formatted as a string

### "break:" macro
If a line to be run starts with "break:", the program will pring everything following break: and then exit the program, marking the current package as finished
