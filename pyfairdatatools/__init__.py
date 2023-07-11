from importlib.metadata import PackageNotFoundError, version

from . import generate, utils, validate

try:
    __version__ = version("pyfairdatatools")
except PackageNotFoundError:
    __version__ = "(local)"

del PackageNotFoundError
del version
