import unittest
import pathlib

from shutil import rmtree
import utils

def setUp(argv: list[str]) -> None:
    for f in argv:
        p = pathlib.Path(f).absolute()
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
        p = pathlib.Path(f)
        if p.exists():
            if p.is_file():
                p.unlink()
                if pathlib.Path(p.parts[0]).is_dir():
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
            fp = pathlib.Path(f)
            self.assertFalse(fp.exists(), "Cleaned up temp files shouldn't exist")


if __name__ == "__main__":
    unittest.main()
