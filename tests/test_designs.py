import pytest
import logging

from reddit2instagram.design import DesignCollection
from ._utils import log_records_below


BUNDELED_DESIGNS = set()


@log_records_below(logging.WARNING)
def test_bundled_search():
    """ Searching and importing bundled modules should never fail. """

    designs = DesignCollection()
    designs.search_bundled_designs()

    found = {design.info.name for design in designs}

    if found != BUNDELED_DESIGNS:
        pytest.fail('\n'.join((
            "Designs found:",
            str(found),
            "Doesn't match expected:",
            str(BUNDELED_DESIGNS)
        )))
