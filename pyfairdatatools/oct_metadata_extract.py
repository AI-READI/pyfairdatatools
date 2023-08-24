import csv
import os

import pydicom


def save_dicom_info_as_tsv(files, output_file):
    """
    Save selected DICOM metadata as a TSV (Tab-Separated Values) file.

    This function takes a list of DICOM files and extracts selected metadata from each file.
    The extracted information includes the data domain (DICOM or not), modality (e.g., OCT),
    patient ID, laterality, manufacturer, file path, and acquisition datetime. The extracted
    metadata is then saved in a TSV file with appropriate columns.

    Args:
        files (list): List of paths to input DICOM files.
        output_file (str): Path to the output TSV file to be created.

    """
    with open(output_file, "w", newline="") as tsv_file:
        writer = csv.writer(tsv_file, delimiter="\t")
        writer.writerow(
            [
                "domain",
                "modality",
                "patient_id",
                "laterality",
                "manufacturer",
                "filepath",
                "acquisitiondatetime",
            ]
        )

        for file in files:
            data_dict = {}
            try:
                dicom = pydicom.dcmread(file)
                data_dict["domain"] = "DICOM"
                if dicom.SOPClassUID == "1.2.840.10008.5.1.4.1.1.77.1.5.4":
                    data_dict["modality"] = "OCT"
                else:
                    data_dict["modality"] = "not OCT"
                data_dict["patient_id"] = dicom.PatientID
                data_dict["laterality"] = dicom.ImageLaterality
                data_dict["manufacturer"] = dicom.Manufacturer
                data_dict["filepath"] = os.path.abspath(file)
                data_dict[
                    "acquisitiondatetime"
                ] = dicom.AcquisitionDateTime  # Use get() with a default value

            except pydicom.errors.InvalidDicomError:
                data_dict["domain"] = "Not DICOM"

            writer.writerow(data_dict.values())
