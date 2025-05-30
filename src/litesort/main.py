#!/usr/bin/python3

import argparse, os, sys
from shutil import copy2, move
from pathlib import Path

from . import utils

VERSION = "0.1.1"
PROGNAME = "lite-sort"

DEFAULT_MAX_DEPTH = 4
DEFAULT_CONFIG: dict = {
    # Read files to sort from this
    "file_list": None,
    # Maximum depth to search for files to sort
    "max_depth": DEFAULT_MAX_DEPTH,
    "move": False,
    "verbose": True,
    # Search directory to find files to sort
    "search_dir": Path.cwd(),
    "dest_dir": Path.cwd(),
    # Files to be sorted, will be merged with entries in `file_list`
    "files": [],
}


def run():
    main(sys.argv[1:])


def main(argv: list[str]) -> None:
    config = DEFAULT_CONFIG
    parse_args(argv, config)

    files_by_type: dict = {
        "archive": [],
        "audio": [],
        "document": [],
        "executable": [],
        "image": [],
        "raw_data": [],
        "video": [],
        "text": [],
    }
    # This will contain all collected files
    file_paths: list[Path] = []

    utils.collect_files(
        search_dir=config["search_dir"],
        current_depth=1,
        config=config,
        file_paths=file_paths,
    )
    utils.sieve_files(config, file_paths, files_by_type)

    cwd = config["search_dir"]
    print(config["dest_dir"])
    lsort(files_by_type, config)


def lsort(files_by_type: dict, config: dict):
    dest_dir = config["dest_dir"]

    for file_type, files in files_by_type.items():
        if len(files) > 0:
            if config["verbose"]:
                print("in %s" % file_type.upper())

            resolved_type_dir = dest_dir / file_type
            if not resolved_type_dir.exists():
                resolved_type_dir.mkdir()

            for f in files:
                dst = dest_dir / file_type / f.parts[-1]

                if config["verbose"]:
                    print("   %s -> %s" % (str(f), str(dst)))

                print("move:", config["move"])
                if config["move"]:
                    os.replace(f, dst)
                else:
                    copy2(f, dst, follow_symlinks=False)

            if config["verbose"]:
                print()
            else:
                print("  \\_ %s" % file_type)


def parse_args(argv: list[str], config: dict) -> None:
    parser = argparse.ArgumentParser(
        prog=PROGNAME,
        description="Collect and sort files in a given directory into directories matching (or relevant to) their filetype.",
        epilog="",
    )
    parser.add_argument(
        "files",
        metavar="FILES",
        help="Files to sort. With no files provided, sorts files starting from the current directory and its subdirectories.",
        nargs="*",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--search-dir",
        metavar="START_DIR",
        help="search directory, where files to be sorted are searched",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--dest-dir",
        metavar="DEST_DIR",
        help="destination directory, where files to be sorted are moved to",
        type=str,
    )
    parser.add_argument(
        "-D",
        "--max-depth",
        metavar="MAX_DEPTH",
        help="maximum filesystem directory depth to search for files",
        type=int,
    )
    parser.add_argument(
        "-f",
        "--file-list",
        metavar="FILE",
        help="file containing list of files to be sorted, files in this list will be merged\n\
              with the [FILES] passed as arguments\n",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--move",
        help="move the files instead of copying them",
        action="store_true",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_false",
        help="no verbose output",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%s %s" % (PROGNAME, VERSION),
    )

    args = parser.parse_args(argv)

    if args.file_list:
        config["file_list"] = Path(args.file_list)

    if args.max_depth:
        config["max_depth"] = args.max_depth

    if args.search_dir:
        dir = Path(args.search_dir)
        if dir.exists():
            config["search_dir"] = dir.absolute()
        else:
            print(
                "%s: error: directory '%s' doesn't exist." % (PROGNAME, str(dir)),
                file=sys.stderr,
            )
            exit(1)
    if args.dest_dir:
        dir = Path(args.dest_dir)
        if dir.exists():
            config["dest_dir"] = dir.absolute()
        else:
            print(
                "%s: error: directory '%s' doesn't exist." % (PROGNAME, str(dir)),
                file=sys.stderr,
            )
            exit(1)

    if len(args.files) == 0:
        print("%s: doing nothing since no files were specified.\n" % PROGNAME)
        parser.print_help()
        exit(0)

    config["files"].extend(args.files)

    if config["file_list"]:
        utils.merge_filelist(config)

    config["move"] = args.move
    config["verbose"] = not args.quiet
