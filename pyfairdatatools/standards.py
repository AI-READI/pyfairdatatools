from abc import abstractmethod


class DataDomain:
    """
    Abstract base class for defining data domain implementations.

    This class defines an abstract interface for data domain implementations. Subclasses
    are expected to provide concrete implementations for the 'convert' and 'metadata' methods.

    Methods:
        convert(infile, outfile, **kwargs): Abstract method to convert data from an input file to an output file.
        metadata(files, outfile, **kwargs): Abstract method to extract metadata from files and save it.
    """

    def __init__(self):
        """
        Initialize the base class for data domain implementations.
        """
        print("in standards init")

    @abstractmethod
    def convert(self, infile, outfile, **kwargs):
        """
        Convert data from an input file to an output file.

        This method is an abstract method that must be overridden in concrete subclasses.

        Args:
            infile (str): Path to the input file.
            outfile (str): Path to the output file.
            **kwargs: Additional keyword arguments specific to the implementation.

        """
        pass

    @abstractmethod
    def metadata(self, files, outfile, **kwargs):
        """
        Extract metadata from files and save it.

        This method is an abstract method that must be overridden in concrete subclasses.

        Args:
            files (list): List of input file paths.
            outfile (str): Path to the output file for saving metadata.
            **kwargs: Additional keyword arguments specific to the implementation.

        """
        pass
