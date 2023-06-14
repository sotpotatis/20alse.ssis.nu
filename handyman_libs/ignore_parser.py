"""ignore_parser.py
The ignore_parser.py parses a possible .handymanignore file in a directory."""
# Implement parsing exception
import os.path
from typing import Optional, List, Callable
from pathlib import Path

class ParsingException(Exception):
    pass

class HandymanIgnoreParser:
    SUPPORTED_PARSER_VERSIONS = [1]

    def __init__(self, version:Optional[int]=None)->None:
        """Create a parser for parsing the ROUTES file.

        :param version: The version of the parser to run. Currently only v1 is supported"""
        if version is None:
            version = 1
        elif version not in HandymanIgnoreParser.SUPPORTED_PARSER_VERSIONS:
            raise ValueError("Unsupported parser version.")
        self.version = version

    def parse_line(self, line:str, base_path:str)->Optional[Callable]:
        """Parses a single line of the .handymanignore file.

         :param line: The input line to parse.

         :param base_path: The base path that we are running in.

         :returns None if the line contains a comment. Otherwise, a function that give
        either True or False where True is ignore and False is do not ignore based on the inputted RELATIVE path."""
        # Check if the line contains a comment
        line = line.strip()
        if line.startswith("#"):
            return None
        else:
            # Try to parse the line
            if line.startswith("(dir)"):
                line = line.replace("(dir)", "").strip()
                # Return a function matching against any children
                return lambda path: Path(line) in Path(os.path.join(base_path, path)).parents
            elif line.startswith("(file)"):
                line = line.replace("(file)", "").strip()
                # Return a function
                return lambda path: Path(os.path.join(base_path, path)).name == line
            else:
                raise ParsingException(f"Invalid start of .handymanignore line: {line} does not start with (dir) or (file) declaration.")

    def find_ignored_files(self, path:str)->List[Callable[[str], bool]]:
        """Finds a possible .handymanignore file in a path and returns a list of functions that give
        either True or False where True is ignore and False is do not ignore based on the inputted RELATIVE path.

        :param path: The path to run in."""
        handymanignore_path = os.path.join(path, ".handymanignore")
        if not os.path.exists(handymanignore_path):
            return []
        else:
            ignore_functions = []
            with open(handymanignore_path, "r") as handymanignore:
                for line in handymanignore.read().splitlines():
                    ignore_function = self.parse_line(line, path)
                    if ignore_function is not None: # None is returned if we are parsing a comment
                        ignore_functions.append(ignore_function)
            return ignore_functions

    def remove_ignored_files_in(self, path:str, ignored_files:List[Callable[[str], bool]], base_directory:Optional[str]=None):
        """Iterates over a path and removes all ignored files that the function can find.

        :param path: The input directory to look in and remove files from if applicable.

        :param ignored_files Output of find_ignored_files used to find files to ignore. Must be ran from the same
        path as the path argument here.

        :param base_directory Optional argument used for recursion."""
        # Handle base_directory path used for recursion.
        if base_directory is None:
            base_directory = ""
        else:
            base_directory = base_directory.rstrip("/") + "/"
        for relative_filepath in os.listdir(path):
            full_filepath = os.path.join(path, base_directory, relative_filepath)
            if os.path.isdir(full_filepath): # Run recursively
                self.remove_ignored_files_in(full_filepath, ignored_files)
            else:
                 # Run all functions and check output
                if any([ignored_files_function(full_filepath) for ignored_files_function in ignored_files]):
                    os.remove(full_filepath) # Remove the filepath