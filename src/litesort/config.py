from pathlib import Path

VERSION = "0.1.2"
PROGNAME = "lite-sort"

DEFAULT_MAX_DEPTH = 4

class Config:
    def __init__(cfg):
        # Search directory to find files to sort
        cfg.search_dir = Path.cwd()
        cfg.dest_dir = Path.cwd()

        # Maximum depth to search for files to sort
        cfg.max_depth = DEFAULT_MAX_DEPTH
        cfg.move = False
        cfg.verbose = True

        # Files to be sorted, will be merged with entries in `file_list`
        cfg.files = []

        cfg.globs = []

        # Read files to sort from this
        cfg.file_list = None
