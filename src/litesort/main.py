#!/usr/bin/python3

import os, sys
from shutil import copy2, move
from pathlib import Path

from . import utils
from .argparse import parse_args
from .config import *
from .filetype import FileType as FT

def run():
    main(sys.argv[1:])


def main(argv: list[str]) -> None:
    config = Config()
    parse_args(argv, config)

    files_by_type: dict[FT, list[Path]] = {
        FT.ARCHIVE:    [],
        FT.AUDIO:      [],
        FT.DOCUMENT:   [],
        FT.EXECUTABLE: [],
        FT.IMAGE:      [],
        FT.RAW_DATA:   [],
        FT.TEXT:       [],
        FT.VIDEO:      [],
    }
    # This will contain all collected files
    file_paths: list[Path] = []

    utils.collect_files(
        search_dir=config.search_dir,
        current_depth=1,
        config=config,
        file_paths=file_paths,
    )
    utils.categorise_files(config, file_paths, files_by_type)

    cwd = config.search_dir
    print(config.dest_dir)
    lsort(files_by_type, config)


def lsort(files_by_type: dict[FT, list[Path]], config: Config):
    dest_dir = config.dest_dir

    for ft, files in files_by_type.items():
        file_type = str(ft)
        if len(files) > 0:
            if config.verbose:
                print("in %s" % file_type)

            resolved_type_dir = dest_dir / file_type
            if not resolved_type_dir.exists():
                resolved_type_dir.mkdir()

            for f in files:
                dst = dest_dir / file_type / f.parts[-1]

                if config.verbose:
                    print("   %s -> %s" % (str(f), str(dst)))

                print("move:", config.move)
                if config.move:
                    os.replace(f, dst)
                else:
                    copy2(f, dst, follow_symlinks=False)

            if config.verbose:
                print()
            else:
                print("  \\_ %s" % file_type)
