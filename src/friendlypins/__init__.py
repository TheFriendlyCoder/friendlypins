"""Package definition for the project"""
import logging
from .version import __version__

logging.getLogger(__name__).addHandler(logging.NullHandler())
