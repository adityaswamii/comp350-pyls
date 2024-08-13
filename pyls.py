import argparse
import os
import time

parser = argparse.ArgumentParser(
    prog="pyls",
    description="Lists files and folders in specified directory",
    epilog="Thanks for using pyls!"
)

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

args = parser.parse_args()


def main(args):
    """
    Prints the list of files and folders in the directory "dirname",
    formatted as per the specifications of "long_format" and "filetype".
    
    :param args:
        args.dirname = The directory whose contents are to be listed.
        args.long_format = True if the user has asked for the long format.
        args.filetype = True if the user has asked for file type info as well.
    :return:
        The main function returns various auxiliary functions
    """
    
    assert isinstance(args.dirname, str), "dirname should be a string"
    assert isinstance(args.long_format, bool), "long_format should be a boolean value"
    assert isinstance(args.filetype, bool), "filetype should be a boolean value"
    
    results = getDescriptionsOfFilesInDir(args.dirname)
    
    assert isinstance(results, list), "results should be a list containing dictionaries"
    assert all(isinstance(contents, dict) for contents in results), "results should be a list containing dictionaries"
    
    lines = formatResults(results, args.long_format, args.filetype)

    assert isinstance(lines, list), "lines should be a list containing strings"
    assert all(isinstance(contents, str) for contents in lines), "lines should be a list containing strings"
    
    printResults(lines)


def getDescriptionsOfFilesInDir(dirname):
    """
    Lists the files and folders in the given directory and constructs a list of dicts with the required
    information. Always fetches all the details required for "long format" presentation for simplicity.
    
    :param dirname:
        The directory whose contents are to be listed.
    :return:
        The return value is a list of dictionaries each with the following keys -
        "filename" = The name of the file.
        "filetype" = "d", "f", or "x" indicating "directory", "plain file",
                 or "executable file" respectively.
        "modtime" = Last modified time of the file as a `datetime` object.
        "filesize" = Number of bytes in the file.
    """

    assert isinstance(dirname, str), "dirname should be a string"
    assert os.path.exists(dirname), "dirname path does not exist"
    
    results = []
    
    for entry in os.scandir(dirname):
        fname = entry.name
        
        ftype = 'f' # It's a file
        if entry.is_dir(follow_symlinks=False):
            ftype = 'd'  # It's a directory
        elif os.access(entry.path, os.X_OK):
            ftype = 'x'  # It's executable
            
        mtime = time.ctime(os.path.getmtime(entry))
        
        fsize = entry.stat(follow_symlinks=False).st_size
        
        entrydict = {
            "filename": fname,
            "filetype": ftype,
            "modtime": mtime,
            "filesize": fsize,
        }
        results.append(entrydict)
    
    return results
    
    # SAMPLE OUTPUT:
    # return [
    #     {
    #         "filename": "file1.txt",
    #         "filetype": "f",
    #         "modtime": datetime(2024, 8, 8, 10, 12, 22),
    #         "filesize": 3658,
    #     },
    #     {
    #         "filename": "pyls",
    #         "filetype": "x",
    #         "modtime": datetime(2024, 8, 9, 14, 33, 25),
    #         "filesize": 2554,
    #     },
    #     {
    #         "filename": "tests",
    #         "filetype": "d",
    #         "modtime": datetime(2024, 8, 9, 15, 15, 15),
    #         "filesize": 355,
    #     },
    # ]


def formatResults(results, long_format, filetype):
    """
    Takes a list of file descriptions and display control flags and
    returns a list of formatted strings, one per line of output.
    
    :param results:
        List of dictionaries, like returned by getDescriptionsOfFilesInDir()
    :param long_format:
        Boolean that indicates long format output.
    :param filetype:
        Boolean that indicates ask for extra type descriptor character at end.
    :return:
        List of strings.
    """

    assert isinstance(long_format, bool), "long_format should be a boolean value"
    assert isinstance(filetype, bool), "filetype should be a boolean value"
    assert isinstance(results, list), "results should be a list containing dictionaries"
    assert all(isinstance(contents, dict) for contents in results), "results should be a list containing dictionaries"

    if long_format:
        print()
    if filetype:
        print()
        
    return results


def printResults(lines):
    """
    Takes a list of line and prints them all to the standard output.
    
    :param lines:
        List of strings
    :return:
        Standard output
    """

    assert isinstance(lines, list), "lines should be a list containing strings"
    assert all(isinstance(contents, str) for contents in lines), "lines should be a list containing strings"
    
    for line in lines:
        print(line)


main(args)
