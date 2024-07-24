#!/usr/bin/env python3

import sys
from pathlib import Path


DEFAULT_CONFIG = {
    # Read files to sort from this
    "file_list": None,
    # Maximum depth to search for files to sort
    "max_depth": 4,
    # Start directory to start searching
    "start_dir": Path.cwd(),
    # Files to be sorted, will be merged with entries in `file_list`
    "files": [],
}


def main(argv):
    config = DEFAULT_CONFIG

    parse_args(argv, config)


def usage(arg0="lite-sort"):
    usage = """\
Usage: %s [options] [files]

With no files provided, sorts files starting from the current directory and its subdirectories.

-d, --start-dir   start directory, where files to be sorted are searched
-D, --max-depth   maximum filesystem directory depth to search for files
-f, --file-list   file containing list of files to be sorted, files in this
                  list will be merged with the [files] passed as arguments
-h, --help        display this help and exit
-v, --version     output version information and exit
"""
    print(usage % arg0, file=sys.stderr)


def parse_args(argv, config):
    argc = len(argv)

    # regular operations
    for i in range(1, argc):
        arg = argv[i]

        if arg == "-h" or arg == "--help":
            usage(argv[0])
            exit(0)
        elif arg == "-f" or arg == "--file-list":
            if i + 1 == argc:
                print(f"lite-sort: --file-list: no file provided", file=sys.stderr)
                usage(argv[0])
                exit(1)
            if argv[i + 1] == "-h" or argv[i + 1] == "--help":
                usage(argv[0])
                exit(0)

            config["file_list"] = Path(argv[i + 1])
        elif arg == "-D" or arg == "--max-depth":
            pass
        else:
            # no other arguments supported, i.e the last parameter is the directory to look in
            dir = Path(arg)
            if dir.exists():
                config["start_dir"] = dir
            else:
                print("directory '%(dir)s' doesn't exist." % {"dir": str(dir)}, file=sys.stderr)

    print(config)


def prep_test_args(argv):
    for f in argv:
        p = Path(f)
        if not p.exists():
            ps = f.split("/")
            if len(ps) > 1:
                maybe_f = Path(ps[-1])
                dirs = Path("/".join(ps[:-1]))
                dirs.mkdir(parents=True)
                if maybe_f.is_dir():
                    (dirs / maybe_f).mkdir()
                else:
                    (dirs / maybe_f).touch()
            else:
                if p.is_dir():
                    p.mkdir()
                else:
                    p.touch()


def clean_test_args(argv):
    # TODO: Implement using os.walk()
    for f in argv:
        p = Path(f)
        if p.exists():
            dirs = f.split("/")
            if len(dirs) > 1:
                if p.is_file():
                    p.unlink(), dirs.pop()
                for i in range(0, len(dirs)):
                    Path("/".join(dirs)).rmdir(), dirs.pop()
            else:
                p.rmdir() if p.is_dir() else p.unlink()


test = False
test_argv = [
    "test",
    "file1.txt",
    "file2.pdf",
    "file3.zip",
    "dir1/file4.xz",
    "dir2/dir21/dir211/dir",
]


if __name__ == "__main__":
    argv = test_argv if test else sys.argv

    if test:
        prep_test_args(test_argv[1:])

    main(argv)

    clean_test_args(test_argv[1:]) if test else None
