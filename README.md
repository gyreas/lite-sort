# lite-sort
`lite-sort` is a simple program to collect and sort files in a given directory into directories
matching (or relevant to) their filetype. Filetype is typically determined by the file's extension,
but falls back to using file header to resolve files without extensions.

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

-f, --file-list   file containing list of files to be sorted, files in this
                  list will be merged with the [files] passed as arguments
-d, --start-dir   start directory, where files to be sorted are searched
-D, --max-depth   maximum filesystem directory depth to search for files
-h, --help        display this help and exit
-v, --version     output version information and exit
```

