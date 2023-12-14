import sys

from cfpir_converter import convert_zip_dicom
from cfpir_metadata_extract import save_dicom_info_as_tsv
from standards import DataDomain


class cfpir(DataDomain):
    """
    Custom data domain class for CFP/IR DICOM data.

    This class inherits from the DataDomain class and defines methods to convert and extract
    metadata from CFP/IR DICOM data files.

    Inherits:
        DataDomain (class): Base class for data domain implementation.

    Methods:
        convert(infile, outfile): Converts a CFP/IR DICOM file to the right format.
        metadata(files, outfile): Extracts metadata from CFP/IR DICOM files and saves it as a TSV file.
    """

    def __init__(self):
        super().__init__()

    def convert(self, infile, outfile):
        """
        Convert a CFP/IR DICOM file to the right format.

        Args:
            infile (str): Path to the input CFP/IR DICOM file.
            outfile (str): Path to the output converted file.
        """

        convert_zip_dicom(infile, outfile)

    def metadata(self, files, outfile):
        """
        Extract metadata from CFP/IR DICOM files and save as a TSV file.

        Args:
            files (list): List of paths to input CFP/IR DICOM files.
            outfile (str): Path to the output TSV file.
        """
        save_dicom_info_as_tsv(files, outfile)
