import argparse, os, sys
from pathlib import Path
from shutil import copy2, move, rmtree
from typing import List, Set, Tuple, Union

from .filetype import FileType
from .config import Config

def categorise_files(
    config: Config,
    file_paths: list[Path],
    files_by_type: dict[FileType, list[Path]]
) -> None:
    # TODO: improve this with the file header especially for files without extension
    # TODO: look into mimetypes
    for f in file_paths:
        ft = categorise_by_filetype(f)
        assert ft != FileType.UNKNOWN, "This is a bug"
        files_by_type[ft].append(f)

def categorise_by_filetype(f: Path) -> FileType:
        ft = FileType.UNKNOWN
        match get_ext(f):
            case ".xz" | ".tar" | ".tar.gz" | ".zip" | ".zstd" | ".rar" | ".gz" | ".lzma":
                ft = FileType.ARCHIVE
            case ".mp3" | ".wav" | ".ogg" | ".m4a":
                ft = FileType.AUDIO
            case ".docx" | ".doc" | ".xls" | ".ppt" | ".pdf" | ".epub" | ".djvu" | ".mobi" | ".odt" | ".xlsx":
                ft = FileType.DOCUMENT
            case ".exe" | ".o" | ".so" | ".a":
                ft = FileType.EXECUTABLE
            case ".png" | ".svg" | ".jpg" | ".jpeg" | ".ppm" | ".xpm" | ".gif" | ".tiff" | ".raw":
                ft = FileType.IMAGE
            case ".iso" | ".data" | ".bin" | ".qcow" | ".qcow2" | ".vdi" | ".vmdk" | ".vhd" | ".hdd":
                ft = FileType.RAW_DATA
            case ".mp4" | ".mkv" | ".mov" | ".avi" | ".3gp" | ".webm" | ".m4v":
                ft = FileType.VIDEO
            case _:
                ft = FileType.TEXT
        return ft

def collect_files(
    search_dir: Path,
    current_depth: int,
    config: Config,
    file_paths: list[Path]
) -> None:
    """
    Walk the path (which is a directory), and collect any files in it into `file_paths`.
    It enumerates `search_dir` on each call.
    """

    if current_depth > config.max_depth:
        return

    # enumerate the current directory
    next_ = next(walk(search_dir, follow_symlinks=False, on_error=print))
    if not next_:
        return

    root, dirs, files = next_

    # combine the matched filepaths with the globs to make it holistic
    fileset: Set[Path] = set(config.files)
    for g in config.globs:
        globs = list(Path(root).glob(g))
        fileset.update(globs)
        del globs

    # collect the (toplevel) regular files here
    for f in files:
        fp = root / f
        assert fp.is_file(), "This is a bug"
        if fp in fileset:
            print("found: %s" % str(fp))
            file_paths.append(fp)

    del files
    del fileset

    # deal with the subdirectories
    for dir in dirs:
        if not Path(dir).stem.startswith('.'):
            collect_files(root / dir, current_depth + 1, config, file_paths)
    del dirs

def merge_filelist(config: Config) -> None:
    """
    Assumes files are in the current directory or its children.
    """
    with open(config.file_list, "r") as file_list:
        files_from_list = list(map(lambda line: line.strip(), file_list.readlines()))
        config.files.extend(files_from_list)

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

# TODO: make the returned tuple of iterables instead
def filter_globs(paths: List[Union[str, Path]]) -> Tuple[List[Path], List[str]]:
    files: List[Path] = []
    globs: List[str] = []

    for p_ in paths:
        p = Path(p_)
        if p.name.find('*') == -1:
            files.append(p)
        else:
            globs.append(str(p_))

    return (files, globs)
