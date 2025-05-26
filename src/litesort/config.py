VERSION = "0.0.1"
PROGNAME = "lite-sort"

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 0:
        if sys.argv[1] == 'v':
            print(VERSION)
