# Created by Patrick Kao
import argparse
import json5
import os
from collections import OrderedDict
import subprocess
from subprocess import Popen
from pathlib import Path
import distutils.dir_util
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


def update_progress(progress, name, script_loc):
    # Update progress file
    progress.append(name)
    list_to_file("{}/progress.txt".format(script_loc), progress)


def install_pack(progress, name, script_loc, package):
    print("[Installer] Installing package {}".format(name))
    # Run line
    for line in package:
        print(">>{}".format(line))
        # Check for macros
        if 'break:' in line:
            print(line.replace('break:', ''))
            update_progress(progress, name, script_loc)
            return
        else:
            split = line.split(" ")
            # Sys.stdin and sys.stdout instead of PIPE redirect output
            command = Popen(line, executable='bash', shell=True, stdin=sys.stdin, stdout=sys.stdout,
                            universal_newlines=True)
            command.communicate()
            result = command.returncode
            if result != 0:
                raise SystemError("Package {} failed installing at line {}".format(name, line))

    update_progress(progress, name, script_loc)


def install_packages():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--workdir", default="/home/{}/temp".format(os.getenv('USER')), type=str,
                        help="Working directory")
    parser.add_argument("--ignore-progress", default=False, type=bool, help="Don't install the same package twice")
    parser.add_argument(
        "--packages",
        nargs="*",  # 0 or more values expected => creates a list
        type=str,
        default=None,  # default if nothing is provided
        help="Install specific packages provided by list (ignores progress but adds to progress)"
    )
    parser.add_argument("--file", default="./packages.json5", type=str,
                        help="Path to json file that contains packages to install")

    args = parser.parse_args()

    script_loc = os.getcwd()
    # load package dict
    with open(args.file, 'r') as file:
        packages = json5.load(file, object_pairs_hook=OrderedDict)

    # load progress list
    progress_file = "{}/progress.txt".format(script_loc)
    Path(progress_file).touch()
    progress = file_to_list(progress_file)

    # Make and switch to workng directory
    os.system("mkdir -p {}".format(args.workdir))
    # Copy resources into workdir
    distutils.dir_util.copy_tree("{}/resources".format(os.getcwd()), "{}".format(args.workdir))

    os.chdir(args.workdir)

    if args.packages is not None:
        for package in args.packages:
            if package in packages:
                install_pack(progress, package, script_loc, packages[package])
            else:
                print("[Installer] Could not find package {} in JSON".format(package))
    else:
        # Iterate through packages
        for name, package in packages.items():
            # check progress
            if (name in progress) and (not args.ignore_progress):
                print("[Installer] Already installed package {}. Skipping".format(name))
                continue

            install_pack(progress, name, script_loc, package)


if __name__ == "__main__":
    install_packages()
