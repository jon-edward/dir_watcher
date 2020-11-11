import os
from typing import Iterable, List


def get_file_extension(path_to_file):
    """
    Returns the extension of a file specified by its path.
    """
    _, extension = os.path.splitext(path_to_file)
    return extension


def list_top_level_of_directory(path_to_directory: str, accepted_extensions: Iterable = None,
                                excluded_extensions: Iterable = None) -> List[str]:
    """
    List the top level paths of a path to a directory, does allow for filtering based on whitelisted and blacklisted
    extensions.

    Including "" in excluded extensions or included extensions will exclude directories from output or include
    directories in output, respectively.
    """

    if accepted_extensions and excluded_extensions:
        raise Exception("Cannot specify both accepted extensions and excluded extensions - use one or the other.")

    unfiltered_items_in_directory = os.listdir(path_to_directory)

    if accepted_extensions:
        accepted_files = [file for file in unfiltered_items_in_directory if
                          get_file_extension(file) in accepted_extensions]
        return accepted_files

    elif excluded_extensions:
        accepted_files = [file for file in unfiltered_items_in_directory if
                          get_file_extension(file) not in excluded_extensions]
        return accepted_files

    else:
        return unfiltered_items_in_directory


def list_nested_directories(path_to_directory: str, accepted_extensions: Iterable = None,
                            excluded_extensions: Iterable = None) -> List[str]:
    """
    List the nested items in specified path to directory, and also items nested in directories under specified path.
    You can exclusively whitelist or blacklist items in directories.

    Including "" in excluded extensions or included extensions will exclude directories from output or include
    directories in output, respectively.
    """

    if accepted_extensions and excluded_extensions:
        raise Exception("Cannot specify both accepted extensions and excluded extensions - use one or the other.")

    nested_path_walker = os.walk(path_to_directory)

    if accepted_extensions:
        accepted_files = []
        for step in nested_path_walker:
            if not get_file_extension(step[0]):
                root = os.path.relpath(step[0], path_to_directory)
            else:
                root = "."
            if "" in accepted_extensions and root != ".":
                accepted_files.append(root)
            for file in step[2]:
                extension = get_file_extension(file)
                if extension in accepted_extensions:
                    if root != ".":
                        accepted_files.append(os.path.join(root, file))
                    else:
                        accepted_files.append(file)
        return accepted_files

    elif excluded_extensions:
        accepted_files = []
        for step in nested_path_walker:
            if not get_file_extension(step[0]):
                root = os.path.relpath(step[0], path_to_directory)
            else:
                root = "."
            if "" not in excluded_extensions and root != ".":
                accepted_files.append(root)
            for file in step[2]:
                extension = get_file_extension(file)
                if extension not in excluded_extensions:
                    if root != ".":
                        accepted_files.append(os.path.join(root, file))
                    else:
                        accepted_files.append(file)
        return accepted_files

    else:
        accepted_files = []
        for step in nested_path_walker:
            if not get_file_extension(step[0]):
                root = os.path.relpath(step[0], path_to_directory)
            else:
                root = "."
            if root != ".":
                accepted_files.append(root)
            for file in step[2]:
                if root != ".":
                    accepted_files.append(os.path.join(root, file))
                else:
                    accepted_files.append(file)
        return accepted_files
