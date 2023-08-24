import sys

from oct_converter import convert_dicom
from oct_metadata_extract import save_dicom_info_as_tsv
from standards import DataDomain


class oct(DataDomain):
    """
    Custom data domain class for OCT (Optical Coherence Tomography) DICOM data.

    This class inherits from the DataDomain class and defines methods to convert and extract
    metadata from OCT DICOM data files.

    Inherits:
        DataDomain (class): Base class for data domain implementation.

    Methods:
        convert(infile, outfile): Converts an OCT DICOM file to the right format.
        metadata(files, outfile): Extracts metadata from OCT DICOM files and saves it as a TSV file.
    """

    def __init__(self):
        super().__init__()

    def convert(self, infile, outfile):
        """
        Convert an OCT DICOM file to the right format.

        Args:
            infile (str): Path to the input OCT DICOM file.
            outfile (str): Path to the output converted file.
        """
        convert_dicom(infile, outfile)

    def metadata(self, files, outfile):
        """
        Extract metadata from OCT DICOM files and save as a TSV file.

        Args:
            files (list): List of paths to input OCT DICOM files.
            outfile (str): Path to the output TSV file.
        """
        save_dicom_info_as_tsv(files, outfile)
