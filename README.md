# lite-sort
`lite-sort` is a simple program to collect and sort files in a given directory into directories
matching (or relevant to) their filetype. Filetype is typically determined by the file's extension,
but falls back to using file header to resolve files without extensions. Written with Python3+

## Install (may require a venv)
$ pip install lite-sort

## Examples
```console
$ lite-sort file1.txt file2.pdf file3.zip
~/Documents
 \_ txt/
 \_ pdf/
 \_ zip/
```

```
Usage: lite-sort [options] [files]

With no files provided, sorts files starting from the current directory and its subdirectories.

OPTIONS:
-s, --search-dir START_DIR  search directory, where files to be sorted are searched
-d, --dest-dir DEST_DIR     destination directory, where files to be sorted are moved to
-D, --max-depth DEPTH       maximum filesystem directory depth to search for files
-f, --file-list FILE        file containing list of files to be sorted, files in this
                            list will be merged with the [files] passed as arguments
-h, --help                  display this help and exit
-m, --move                  move the files instead of copying them
-v, --version               output version information and exit
-V, --verbose               verbose output
```
