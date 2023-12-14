import csv
import os

import pydicom


def save_dicom_info_as_tsv(files, output_file):
    """
    Save DICOM metadata information as a TSV file.

    This function takes a list of DICOM files and saves selected metadata information from each file
    into a Tab-Separated Values (TSV) file. The saved information includes domain, modality, patient ID,
    laterality, manufacturer, file path, and acquisition datetime.

    Args:
        files (list): List of paths to the input DICOM files.
        output_file (str): The path to the output TSV file to be created.

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
                data_dict["modality"] = dicom.Modality
                if dicom.SOPClassUID == "1.2.840.10008.5.1.4.1.1.77.1.5.1":
                    data_dict["modality"] = "CFP/IR"
                else:
                    data_dict["modality"] = "not CFP/IR"
                data_dict["patient_id"] = dicom.PatientID
                data_dict["laterality"] = dicom.ImageLaterality
                data_dict["manufacturer"] = dicom.Manufacturer
                data_dict["filepath"] = os.path.abspath(file)
                data_dict["acquisitiondatetime"] = dicom.AcquisitionDateTime
            except pydicom.errors.InvalidDicomError:
                data_dict["domain"] = "Not DICOM"

            writer.writerow(data_dict.values())
