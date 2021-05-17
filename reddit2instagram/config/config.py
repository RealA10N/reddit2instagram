""" This file contains the code that reads and analyses the user config file
and converts it into a `Reddit2Instagram` object instance. """

import typing
import json
import yaml

from reddit2instagram.exceptions import InvalidConfigFileType

ValidFileTypes = {
    "json": json.loads,
    "yaml": yaml.full_load,
    "yml": yaml.full_load,
}


class Config:

    def __init__(self, fp: typing.TextIO, filetype: str = 'yaml'):
        loader = self._loader_from_filetype(filetype)
        self._raw = loader(fp)

    @staticmethod
    def _loader_from_filetype(filetype: str):
        """ Returns a loader function that matches the given filetype string. """

        try:
            return ValidFileTypes[filetype.lower()]

        # Error handeling
        except KeyError as exception:

            # Converts the list of supported filetypes into a readable string
            supported = ', '.join(map(
                lambda s: f"'{s}'",
                ValidFileTypes.keys())
            )

            # Raises an exception with a custom error message.
            raise InvalidConfigFileType(
                f"Invalid filetype {filetype}." +
                f"Supported filetypes are {supported}"
            ) from exception
