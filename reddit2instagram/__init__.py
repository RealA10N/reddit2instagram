from .logger import setup_logger
from .design import Design, DesignInfo, DesignCollection


__version__ = '0.0.1-dev'

__all__ = [
    'Design',
    'DesignInfo',
    'DesignCollection',
]

setup_logger()
