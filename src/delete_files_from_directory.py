import os
import sys
import argparse
from pathlib import Path
from typing import List, Set, Dict


def get_args(argv: List) -> argparse.Namespace:
    """_summary_

    Args:
        argv (List): List of file args

    Returns:
        argparse.Namespace:
    """

    parser = argparse.ArgumentParser(
        prog="delete_files_from_directory.py",
        description="Deletes single or multiple files from a given directory",
    )

    parser.add_argument(
        "--directory",
        "--dir",
        "-d",
        help="Top level directory, containing multiple files or sub directories",
        type=str,
        nargs="?",
        required=True,
    )

    parser.add_argument(
        "--filenames_str",
        "-fs",
        help="Filenames within directories you wish to delete. Delimited with a ',' Example: 'foo.txt' or 'foo.txt,bar.zip,baz.log'",
        type=str,
        nargs="?",
    )

    parser.add_argument(
        "--txt_file_filenames",
        "-tfl",
        help="Filenames within directories you wish to delete. Delimited with a newline.",
        type=str,
        nargs="?",
    )

    return parser.parse_args(argv)


def get_filenames_set(filenames_str: str, txt_file_filenames: str) -> Set[str]:
    """_summary_

    Args:
        filenames_str (str): Comma delimited string of filenames
        txt_file_filenames (str): String of .txt file that contains list of filenames, delimited by a new line

    Raises:
        NameError: If .txt file does not exist

    Returns:
        Set[str]: Set of unique file names
    """

    filenames_str_paths: List[str] = filenames_str.split(",")
    file_set: Set[str] = set(filenames_str_paths)

    if txt_file_filenames != None:
        if not os.path.exists(txt_file_filenames):
            raise NameError(f"File '{txt_file_filenames}' does not exist")
        else:
            with open(txt_file_filenames) as file:
                files: List[str] = [line.rstrip() for line in file]
                file_set = set(filenames_str_paths + files)

    return file_set


def remove_files(directory: str, file_set: Set[str]) -> None:
    """_summary_

    Args:
        directory (str): String of directory path
        file_set (Set[str]): Set of unique file names
    """

    for filename in file_set:
        for file_path in Path(directory).rglob(filename):
            os.remove(file_path)
            print(f"{file_path} deleted")


if __name__ == "__main__":
    args_dict: Dict = get_args(sys.argv[1:]).__dict__

    directory: str = args_dict["directory"]
    filenames_str: str = args_dict["filenames_str"]
    txt_file_filenames: str = args_dict["txt_file_filenames"]

    if not os.path.exists(directory):
        raise NameError(f"Directory '{directory}' does not exist")

    if not filenames_str and not txt_file_filenames:
        raise NameError("Please define the filenames to delete, by using the relevant argument explained by using the \'-h\' flag")
    
    file_set: Set[str] = get_filenames_set(
        filenames_str=filenames_str, txt_file_filenames=txt_file_filenames
    )
    remove_files(directory=directory, file_set=file_set)
