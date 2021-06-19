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
        self.__designs = dict()

    def get_design(self, name: str) -> typing.Optional[Design]:
        """ Returns a design by name from the collected designs. If design with
        the given name is not collected, returns `None`. """

        return self.__designs.get(name)

    def collect_design(self, design: typing.Type[Design]) -> None:
        """ Recives a design object and adds it to the collection. If the given
        object is not a valid design, logs a warning. """

        for test in self.DESIGN_TESTS:
            if not test.run(design):
                logger.warning(test.error, design)
                return

        # If passed all tests
        name = design.info.name
        name_taken = name in self.__designs

        if name_taken:
            logger.warning(
                'Found multiple designs named *%s*... '
                'The first one found will be collected'
            )

        else:
            self.__designs[name] = design
            logger.debug('Collected design *%s*', design.info.name)

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

    def search_bundled_designs(self,) -> None:
        """ Collects the bundled designs that came installed with the installation
        of the base reddit2instagram module. """

        here = os.path.dirname(__file__)
        bundled = os.path.join(here, 'bundled', '__init__.py')

        self.search_designs_in_file(bundled)

    def search_designs_in_file(self, path: str):
        """ Recives a path to a Python file, and tries to load it and import
        the designs located in the `__designs__` variable. If designs are found,
        appends them to the design collection. If something goes wrong, logs an
        error. """

        module = self.__module_from_file(path)

        try:
            designs = module.__designs__

        except AttributeError:
            logger.debug(
                "Found Python file file *%s* without the '__designs__' constant",
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
