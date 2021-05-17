import pytest
from reddit2instagram.config import config


class TestConfig:

    def test_config_filetypes_lowercase(self):
        assert all(map(
            lambda filetype: filetype.islower(),
            config.ValidFileTypes.keys(),
        ))
