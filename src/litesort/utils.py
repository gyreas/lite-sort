import argparse, os, sys
from pathlib import Path
from shutil import copy2, move, rmtree

def sieve_files(config: dict, file_paths: list[Path], files_by_type: dict) -> None:
    # TODO: improve this with the file header especially for files without extension
    # TODO: look into mimetypes
    for f in file_paths:
        match get_ext(f):
            case ".xz" | ".tar" | ".tar.gz" | ".zip" | ".zstd" | ".rar" | ".gz" | ".lzma":
                files_by_type["archive"].append(f)
            case ".mp3" | ".wav" | ".ogg" | ".m4a":
                files_by_type["audio"].append(f)
            case ".docx" | ".doc" | ".xls" | ".ppt" | ".pdf" | ".epub" | ".djvu" | ".mobi" | ".odt" | ".xlsx":
                files_by_type["document"].append(f)
            case ".exe" | ".o" | ".so" | ".a":
                files_by_type["executable"].append(f)
            case ".png" | ".svg" | ".jpg" | ".jpeg" | ".ppm" | ".xpm" | ".gif" | ".tiff" | ".raw":
                files_by_type["image"].append(f)
            case ".iso" | ".data" | ".bin" | ".qcow" | ".qcow2" | ".vdi" | ".vmdk" | ".vhd" | ".hdd":
                files_by_type["raw_data"].append(f)
            case ".mp4" | ".mkv" | ".mov" | ".avi" | ".3gp" | ".webm" | ".m4v":
                files_by_type["video"].append(f)
            case _:
                files_by_type["text"].append(f)


def collect_files(search_dir: Path, current_depth: int, config: dict, file_paths: list[Path]) -> None:
    """
    Walk the path (which is a directory), and collect any files in it into `file_paths`.
    It enumerates `search_dir` on each call.
    """

    if current_depth > config["max_depth"]:
        return

    # enumerate the current directory
    next_ = next(walk(search_dir, follow_symlinks=False, on_error=print))
    if not next_:
        return

    root, dirs, files = next_

    # collect the (toplevel) regular files here
    for f in files:
        fp = root / f
        if fp.is_file():
            if fp.name in config["files"]:
                print("found: %s" % str(fp))
                file_paths.append(fp)
    del files

    # deal with the subdirectories
    for dir in dirs:
        if not Path(dir).stem.startswith("."):
            collect_files(root / dir, current_depth + 1, config, file_paths)
    del dirs

def merge_filelist(config: dict) -> None:
    """Assumes files are in the current directory or its children."""
    with open(config["file_list"], "r") as file_list:
        files_from_list = list(map(lambda line: line.strip(), file_list.readlines()))
        config["files"].extend(files_from_list)

def get_ext(path: Path) -> str:
    return "".join(path.suffixes)

def walk(root, on_error=None, follow_symlinks=False):
    """
    Walk the directory tree from this directory, similar to os.walk().
    """
    paths = [root]
    while paths:
        path = paths.pop()
        if isinstance(path, tuple):
            yield path
            continue
        dirnames = []
        filenames = []
        try:
            for child in path.iterdir():
                try:
                    # if child.is_dir(follow_symlinks=follow_symlinks):
                    if child.is_dir():
                        dirnames.append(child.name)
                    else:
                        filenames.append(child.name)
                except OSError:
                    filenames.append(child.name)
        except OSError as error:
            if on_error is not None:
                on_error(error)
            continue

        yield path, dirnames, filenames
        paths += [path.joinpath(d) for d in reversed(dirnames)]
