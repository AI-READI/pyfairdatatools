from classifying_rules import (
    process_dicom_zip,
    process_ecg_zip,
    process_env_zip,
    process_flio_zip,
)


def data_identifier(zip_file_path):
    if not zip_file_path.endswith(".zip"):
        return "Not a zip file"

    elif "ENV" in zip_file_path:
        return process_env_zip(zip_file_path)

    elif "xml" in zip_file_path:
        return process_ecg_zip(zip_file_path)

    elif "FLIO" in zip_file_path:
        return process_flio_zip(zip_file_path)

    elif any(
        word in zip_file_path
        for word in [
            "Optomed",
            "Eidon",
            "Maestro",
            "Triton",
            "Cirrus",
            "Spectralis",
        ]
    ):
        return process_dicom_zip(zip_file_path)

    else:
        return "Unknown file type"
