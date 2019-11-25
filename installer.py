# Created by Patrick Kao
import argparse
import json5
import os
from collections import OrderedDict
import sys


def list_to_file(filename, list_to_write):
    with open(filename, 'w') as filehandle:
        for listitem in list_to_write:
            filehandle.write('{}\n'.format(listitem))


def file_to_list(filename):
    to_ret = []
    with open(filename, 'r+') as filehandle:  # a+ makes file if not exist
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            to_ret.append(currentPlace)
    return to_ret


def install_packages():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--workdir", default="/home/{}/temp".format(os.getenv('USER')), type=str,
                        help="Working directory")
    parser.add_argument("--ignore-progress", default=False, type=bool, help="Don't install the same package twice")

    args = parser.parse_args()

    script_loc = os.getcwd()
    # load package dict
    with open('./packages.json5', 'r') as file:
        packages = json5.load(file, object_pairs_hook=OrderedDict)

    # load progress list
    progress = file_to_list("{}/progress.txt".format(script_loc))

    # Make and switch to workng directory
    os.system("mkdir -p {}".format(args.workdir))
    os.chdir(args.workdir)

    # Iterate through packages
    for name, package in packages.items():
        # check progress
        if (name in progress) and (not args.ignore_progress):
            print("Already installed package {}. Skipping".format(name))
            continue

        # Run line
        for line in package:
            print(">>{}".format(line))
            # Check for macros
            if 'break:' in line:
                print(line.replace('break:', ''))
            else:
                result = os.system(line)
                if result != 0:
                    raise SystemError("Package {} failed installing at line {}".format(name, line))\

        # Update progress file
        progress.append(name)
        list_to_file("{}/progress.txt".format(script_loc), progress)

if __name__ == "__main__":
    install_packages()
