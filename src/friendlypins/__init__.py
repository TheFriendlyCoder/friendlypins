"""Package definition for the project"""
import logging
import os
import ast

_CUR_FILE = os.path.realpath(__file__)
_CUR_PATH = os.path.split(_CUR_FILE)[0]
_PROPS = open(os.path.join(_CUR_PATH, 'version.prop')).read()
__version__ = ast.literal_eval(_PROPS)

logging.getLogger(__name__).addHandler(logging.NullHandler())
