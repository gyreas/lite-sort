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


class TestGlobCommandline(unittest.TestCase):
    config = TEST_CONFIG
    start = TESTDIR / "start_dir"
    dest = TESTDIR / "dest_dir"
    argv = [
        "-s",
        str(start),
        "-d",
        str(dest),
        "*.txt",
        "a.txt",
        "b.txt",
        "*.py",
        "a.py",
        "b.py",
    ]

    def setUp(self):
        TestGlobCommandline.start.mkdir(parents=True)
        TestGlobCommandline.dest.mkdir(parents=True)
        touch(
            TestGlobCommandline.start,
            ["a.py", "b.py", "c.py", "d.py", "a.txt", "b.txt", "c.txt", "d.txt"],
        )

    def test_do(self):
        parse_args(TestGlobCommandline.argv, TestGlobCommandline.config)

        assert TestGlobCommandline.config.search_dir == TestGlobCommandline.start
        assert TestGlobCommandline.config.dest_dir == TestGlobCommandline.dest

        paths_: List[Path] = []
        utils.collect_files(
            search_dir=TestGlobCommandline.start,
            current_depth=1,
            config=TestGlobCommandline.config,
            file_paths=paths_,
        )
        paths_.sort()
        paths = list(map(lambda p: p.name, paths_))
        del paths_

        print(paths)

        assert paths == [
            "a.py",
            "a.txt",
            "b.py",
            "b.txt",
            "c.py",
            "c.txt",
            "d.py",
            "d.txt",
        ]

    def tearDown(self):
        rmtree(str(TestGlobCommandline.start))
        rmtree(str(TestGlobCommandline.dest))
