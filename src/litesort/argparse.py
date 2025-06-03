import argparse, sys

from . import utils
from .config import *

def parse_args(argv: list[str], config: Config) -> None:
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
        config.file_list = Path(args.file_list)

    if args.max_depth:
        config.max_depth = args.max_depth

    if args.search_dir:
        dir = Path(args.search_dir)
        if dir.exists():
            config.search_dir = dir.absolute()
        else:
            print(
                "%s: error: directory '%s' doesn't exist." % (PROGNAME, str(dir)),
                file=sys.stderr,
            )
            exit(1)
    if args.dest_dir:
        dir = Path(args.dest_dir)
        if dir.exists():
            config.dest_dir = dir.absolute()
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

    files, globs = utils.filter_globs(args.files)
    config.files.extend(files)
    config.globs.extend(globs)

    if config.file_list:
        utils.merge_filelist(config)

    config.move = args.move
    config.verbose = not args.quiet
