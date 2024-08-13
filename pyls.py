import argparse

parser = argparse.ArgumentParser(
    prog="pyls",
    description="Lists files in specified directory"
)

# pyls arguments

parser.add_argument(
    "dirname",
    help="Name of directory to list the contents of",
    action="store",
    nargs="?",
    default=".",
)

parser.add_argument(
    "-l",
    "--long-format",
    help="Presents more details about files in columnar format",
    action="store_true",
)

parser.add_argument(
    "-F",
    "--filetype",
    help="Adds an extra character to the end of the printed filename that indicates its type.",
    action="store_true",
)

