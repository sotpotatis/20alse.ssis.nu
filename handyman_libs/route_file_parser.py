"""routes_file_parser.py
Parses the ROUTES mapping file."""
from typing import Optional, Tuple, List

# Implement parsing exception
class ParsingException(Exception):
    pass

class RoutesFileParser:
    SUPPORTED_PARSER_VERSIONS = [1]

    def __init__(self, source_file_path:str, version:Optional[int]=None)->None:
        """Create a parser for parsing the ROUTES file.

        :param source_file_path: The source filepath for accessing the ROUTES file.
        Must be validated!

        :param version: The version of the parser to run. Currently only v1 is supported"""
        if version is None:
            version = 1
        elif version not in RoutesFileParser.SUPPORTED_PARSER_VERSIONS:
            raise ValueError("Unsupported parser version.")
        self.source_file_path = source_file_path
        self.version = version

    def parse_line(self, line:str)->Optional[Tuple[str, str]]:
        """Parses a single mapping of the ROUTES file.

        :param line: The input line to parse.

        :returns None if the line contains a comment. Otherwise a tuple in the format: repository: mapping.
        Note: If anything goes wrong, an exception is raised."""
        # Check if the line contains a comment
        line = line.strip()
        if line.startswith("#"):
            return None
        else:
            # Try to parse the line
            line_parts = line.split("-->")
            if len(line_parts) == 2:
                source_folder_name, destination_folder_name = line_parts # Unpack
                source_folder_name = source_folder_name.strip("/")
                destination_folder_name = destination_folder_name.strip("/")
                return (source_folder_name, destination_folder_name)
            else:
                raise ParsingException("Failed to parse line: contains more than one arrow (-->)")

    def parse(self)->List[Tuple[str, str]]:
        """Parses the input file.

        :returns A list containing tuples for every routed directory in the format (<input directory name>, <target path>)."""
        output = []  # Create output set
        with open(self.source_file_path, "r") as input_file:
            for line in input_file.read().splitlines():
                mapping = self.parse_line(line)
                if mapping is not None: # None is returned if we are parsing a comment
                    output.append(mapping)
        return output