import typing
import logging
import importlib
import inspect
import os

from dataclasses import dataclass
from reddit2instagram.design import Design, DesignInfo

logger = logging.getLogger(__name__)


@dataclass
class DesignTest:
    # A function that recives a single parameter: the design object
    # and returns `True` if the test passes and `False` if the test
    # Fails.
    run: typing.Callable

    # Error message that would be logged if the test fails
    error: str


class DesignCollection:

    # A collection of tests that will be run before adding any desing to the
    # designs collection.
    DESIGN_TESTS = (
        DesignTest(
            run=inspect.isclass,
            error='Object *%s* is not a valid design object',
        ),
        DesignTest(
            run=lambda design: issubclass(design, Design),
            error='Object *%s* is not a subclass of the *Design* object',
        ),
        DesignTest(
            run=lambda design: not inspect.isabstract(design),
            error='Design object *%s* missing required design features'
        ),
    )

    def __init__(self):
        self.__designs = list()

    def collect_design(self, design: typing.Type[Design]) -> None:
        """ Recives a design object and adds it to the collection. If the given
        object is not a valid design, logs a warning. """

        for test in self.DESIGN_TESTS:
            if not test.run(design):
                logger.warning(test.error, design)
                return

        # If passed all tests
        self.__designs.append(design)
        logger.debug('Collected design object *%s*', design.info.name)

    def search_designs(self, path: str) -> None:
        """ Recives a path to a Python file that contains a collection of designs,
        or a path to a folder that contains multiple Python files. Searchs for
        designs in those Python files, adds the found designs into the design
        collection. """

        paths = [path]

        while paths:
            path: str = paths.pop()

            if os.path.isfile(path) and path.endswith('.py'):
                self.search_designs_in_file(path)

            elif os.path.isdir(path):
                paths += [
                    os.path.join(path, new)
                    for new in os.listdir(path)
                ]

    def search_designs_in_file(self, path: str):
        """ Recives a path to a Python file, and tries to load it and import
        the designs located in the `__designs__` variable. If designs are found,
        appends them to the design collection. If something goes wrong, logs an
        error. """

        module = self.__module_from_file(path)

        try:
            designs = module.__designs__

        except AttributeError:
            logger.warning(
                'While searching for designs, found Python '
                "file *%s* without the '__designs__' constant",
                path
            )

        else:
            for design in designs:
                self.collect_design(design)

    @staticmethod
    def __module_from_file(filepath: str):
        """ Recives a path to a Python file, loads the file as a standalone module
        and returns the loaded module. """

        filename = os.path.basename(filepath)
        name = os.path.splitext(filename)[0]

        spec = importlib.util.spec_from_file_location(
            name=name,
            location=filepath,
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
