from importlib.metadata import PackageNotFoundError, version

from . import generate, utils, validate

try:
    __version__ = version("pyfairdatatools")
except PackageNotFoundError:
    __version__ = "0.1.1"

del PackageNotFoundError
del version
