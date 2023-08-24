from image_classifying_rules import get_dicom_summary, is_dicom_file


def data_identifier(file):
    if file.endswith(".zip"):
        return "Environmental Sensor File"
    elif file.endswith(".xml"):
        return "ECG File"
    elif is_dicom_file(file):
        dicom = get_dicom_summary(file)
        return dicom
    else:
        return "Unknown File Type"
