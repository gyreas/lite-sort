import random
import os
import unittest

from pathlib import Path
from shutil import rmtree
from typing import List, Union

from litesort import utils
from litesort.config import *
from litesort.argparse import parse_args

td = os.getenv("TESTDIR")
TESTDIR = Path(".testdir" if td is None else td).absolute()
TEST_CONFIG = Config()


def setUp(argv: list[str]) -> None:
    for f in argv:
        p = Path(f).absolute()
        if not p.exists():
            if p.is_dir():
                p.mkdir(parents=True)
            else:
                if not p.parent.exists():
                    p.parent.mkdir(parents=True)
                p.touch()
        else:
            p.mkdir(parents=True) if p.is_dir() else p.touch()


def tearDown(argv: list[str]) -> None:
    for f in argv:
        p = Path(f)
        if p.exists():
            if p.is_file():
                p.unlink()
                if Path(p.parts[0]).is_dir():
                    rmtree(p.parts[0])
            else:
                rmtree(p)


class LiteSortError(Exception):
    pass


class TestNoop(unittest.TestCase):
    def test_noop(self):
        self.assertEqual(None, None)


class TestSetupAndDelete(unittest.TestCase):
    test_files = [
        "test",
        "file1.txt",
        "file2.pdf",
        "file3.zip",
        "dir1/d/d/d/d/d/d/d//file4.xz",
        "dir2/dir21/dir211/dir2111/dir21111/not_a_dir",
    ]

    def test__setup_and_delete(self):
        setUp(self.test_files)
        tearDown(self.test_files)

        # make sure they don't exist
        for f in self.test_files:
            fp = Path(f)
            self.assertFalse(fp.exists(), "Cleaned up temp files shouldn't exist")


class TestCanClassify(unittest.TestCase):
    tests = [
        ("text", ["file1.txt"]),
    ]

    def test__can_classify(self):
        pass


def touch(basedir: Union[str, Path], paths: List[Union[str, Path]]) -> None:
    for p_ in paths:
        p = Path(basedir) / Path(p_)
        p.touch()


# I thought I needed this for naming clashing reasons in the test environments, but nah
# I forgot to implement tearDown form nested test case
def h() -> int:
    return random.randint((1 << 32) - 1, (1 << 64) - 1)

class TestGlobCommandline_NestedSearchDir(unittest.TestCase):
    config = TEST_CONFIG
    start = TESTDIR / "start_dir"
    dest = TESTDIR / "dest_dir"

    def setUp(self) -> None:
        self.start.mkdir(parents=True, exist_ok=True)
        self.dest.mkdir(parents=True, exist_ok=True)
        (self.start / "0" / "1").mkdir(parents=True, exist_ok=True)
        touch(self.start / "0" / "1", ["tar.xz", "xz.zip"])

    def runTest(self) -> None:
        argv = [
            "-s",
            str(self.start / "0" / "1"),
            "-d",
            str(self.dest / "DEST"),
            "tar.xz",
            "xz.zip",
        ]
        parse_args(argv, self.config)

        print(self.config.search_dir)
        print(self.config.dest_dir)
        print(self.config.files)

        self.assertEqual(self.config.search_dir, self.start / "0" / "1")
        self.assertEqual(self.config.dest_dir, self.dest / "DEST")

        paths_: List[Path] = []
        utils.collect_files(
            search_dir=self.start,
            current_depth=1,
            config=self.config,
            file_paths=paths_,
        )
        print(paths_)
        paths_.sort()
        paths = list(map(lambda p: p.name, paths_))
        del paths_
        self.assertEqual(paths, ["tar.xz", "xz.zip"])

    def tearDown(self) -> None:
        rmtree(str(self.start))
        rmtree(str(self.dest))


class TestGlobCommandline0(unittest.TestCase):
    config = TEST_CONFIG
    start = TESTDIR / "start_dir"
    dest = TESTDIR / "dest_dir"
    create: List[Union[str, Path]] = [
        "a.py",
        "a.txt",
        "b.py",
        "b.txt",
        "c.py",
        "c.txt",
        "d.py",
        "d.txt",
    ]

    def setUp(self) -> None:
        self.start.mkdir(parents=True, exist_ok=True)
        self.dest.mkdir(parents=True, exist_ok=True)
        touch(
            self.start,
            self.create,
        )

    def runTest(self) -> None:
        argv = [
            "-s",
            str(self.start),
            "-d",
            str(self.dest),
            "*.txt",
            "a.txt",
            "b.txt",
            "*.py",
            "a.py",
            "b.py",
        ]

        parse_args(argv, self.config)

        assert self.config.search_dir == self.start
        assert self.config.dest_dir == self.dest

        paths_: List[Path] = []
        utils.collect_files(
            search_dir=self.start,
            current_depth=1,
            config=self.config,
            file_paths=paths_,
        )
        paths_.sort()
        paths = list(map(lambda p: p.name, paths_))
        del paths_

        self.assertEqual(paths, self.create)

    def tearDown(self) -> None:
        rmtree(str(self.start))
        rmtree(str(self.dest))
