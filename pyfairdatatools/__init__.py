from importlib.metadata import PackageNotFoundError, version

from . import generate, utils, validate

try:
    __version__ = version("pyfairdatatools")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version

from .cfpir import *
from .identifier import *
from .oct import *
from .standards import DataDomain
