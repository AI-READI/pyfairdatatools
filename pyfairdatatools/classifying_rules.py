# type: ignore

import os
import shutil
import tempfile
import zipfile

import pydicom
import xmltodict
from defusedxml import minidom


class ClassifyingRule:
    def __init__(self, name, conditions):
        self.name = name
        self.conditions = conditions

    def apply(self, dicom_entry):
        for condition in self.conditions:
            if not condition(dicom_entry):
                return False
        return True


# List of ClassifyingRule instances
rules = [
    # optomed
    ClassifyingRule(
        "OptoMed_CFP_Disc_or_Mac_centered",
        conditions=[lambda entry: "Aurora" == entry.device],
    ),
    # eidon
    ClassifyingRule(
        "Eidon_UWF_Central_IR",
        conditions=[
            lambda entry: "0-infrared" in entry.filename.lower()
            and "Eidon" in entry.device
        ],
    ),
    ClassifyingRule(
        "Eidon_UWF_Central_FAF",
        conditions=[
            lambda entry: "0-af-" in entry.filename.lower() and "Eidon" in entry.device
        ],
    ),
    ClassifyingRule(
        "Eidon_UWF_Central_CFP",
        conditions=[
            lambda entry: "0-visible" in entry.filename.lower()
            and "Eidon" in entry.device
        ],
    ),
    ClassifyingRule(
        "Eidon_UWF_Nasal_CFP",
        conditions=[
            lambda entry: "3-visible" in entry.filename.lower()
            and "Eidon" in entry.device
        ],
    ),
    ClassifyingRule(
        "Eidon_UWF_Temporal_CFP",
        conditions=[
            lambda entry: "4-visible" in entry.filename.lower()
            and "Eidon" in entry.device
        ],
    ),
    ClassifyingRule(
        "Eidon_UWF_Mosaic_CFP",
        conditions=[
            lambda entry: "11-visible" in entry.filename.lower()
            and "Eidon" in entry.device
        ],
    ),
    # maestro
    ClassifyingRule(
        "Maestro2_3D_Wide_OCT",
        conditions=[
            lambda entry: "3DOCT-1Maestro2" == entry.device
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and str(entry.slicethickness).startswith("0.07")
        ],
    ),
    ClassifyingRule(
        "Maestro2_3D_Macula_OCT",
        conditions=[
            lambda entry: "3DOCT-1Maestro2" == entry.device
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and str(entry.slicethickness).startswith("0.04")
        ],
    ),
    ClassifyingRule(
        "Maestro2_Mac_6x6-360x360_OCTA",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and str(entry.slicethickness).startswith("0.01")
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    # triton
    ClassifyingRule(
        "Triton_3D(H)_Radial_OCT",
        conditions=[
            lambda entry: "fo-dicom 4.0.8" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and str(entry.slicethickness).startswith("0.03")
            and "Triton plus" == entry.device
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness).startswith("0.01")
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness).startswith("0.02")
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    # #spectralis
    ClassifyingRule(
        "Spec_ONH_RC_HR_OCT",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and (not isinstance(entry.framenumber, str))
            and (26 <= int(entry.framenumber) <= 28)
            and str(entry.rows) == "496"
            and str(entry.columns) == "768"
            and entry.slicethickness == ""
        ],
    ),
    ClassifyingRule(
        "Spec_ONH_RC_HR_OCT_reference_IR",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.rows) == "1536"
            and str(entry.columns) == "1536"
        ],
    ),
    ClassifyingRule(
        "Spec_PPole_Mac_HR_OCT",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and (not isinstance(entry.framenumber, str))
            and (60 <= int(entry.framenumber) <= 62)
            and str(entry.rows) == "496"
            and str(entry.columns) == "768"
        ],
    ),
    ClassifyingRule(
        "Spec_PPole_Mac_HR_OCT_reference_IR",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.rows) == "768"
            and str(entry.columns) == "768"
            and str(entry.privatetag) == "N/A"
            and str(entry.gaze) == "R-1022D"
        ],
    ),
    ClassifyingRule(
        "Spec-Mac-20x20-HS_OCTA_reference_Bscan",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and (not isinstance(entry.framenumber, str))
            and (511 <= int(entry.framenumber) <= 513)
            and str(entry.rows) == "496"
            and str(entry.columns) == "512"
        ],
    ),
    ClassifyingRule(
        "Spec-Mac-20x20-HS_OCTA_reference_IR",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.rows) == "768"
            and str(entry.columns) == "768"
            and str(entry.privatetag) == "Super Slim"
        ],
    )
    # OCTA
    # FLIO
]


class DicomEntry:
    def __init__(
        self,
        filename,
        patientid,
        sopclassuid,
        sopinstanceuid,
        laterality,
        rows,
        columns,
        device,
        framenumber,
        referencedsopinstance,
        slicethickness,
        implementationversion,
        gaze,
        privatetag,
        softwareversion,
        numberoffiles,
    ):
        self.filename = filename
        self.patientid = patientid
        self.sopclassuid = sopclassuid
        self.sopinstanceuid = sopinstanceuid
        self.laterality = laterality
        self.rows = rows
        self.columns = columns
        self.device = device

        self.framenumber = framenumber
        self.referencedsopinstance = referencedsopinstance
        self.slicethickness = slicethickness
        self.implementationversion = implementationversion
        self.gaze = gaze
        self.privatetag = privatetag
        self.softwareversion = softwareversion
        self.numberoffiles = numberoffiles


class DicomSummary:
    def __init__(
        self, domain, patientid, laterality, protocol
    ):  # sopinstance, matchingcfpifsopinstance
        self.domain = domain  # DICOM
        self.patientid = patientid  # patient id
        self.laterality = laterality  # laterality
        self.protocol = protocol  # belongs to which one in AIREADI checklist


def extract_dicom_entry(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found.")

    dicom = pydicom.dcmread(file).to_json_dict()
    ds = pydicom.dcmread(file)

    filename = os.path.basename(file)
    patientid = dicom["00100020"]["Value"][0]
    sopclassuid = dicom["00080016"]["Value"][0]
    sopinstanceuid = dicom["00080018"]["Value"][0]

    folder_path = os.path.dirname(file)
    folder_files = os.listdir(folder_path)
    filecount = len(
        [f for f in folder_files if os.path.isfile(os.path.join(folder_path, f))]
    )

    # Fundus photo 2D
    if sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.1":
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        laterality = dicom["00200062"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        softwareversion = dicom["00181020"]["Value"][0]
        numberoffiles = filecount
        if "00511017" in dicom:
            privatetag = dicom["00511017"]["Value"][0]
        else:
            privatetag = "N/A"

        if "00220006" in dicom and "00080100" in dicom["00220006"]["Value"][0]:
            gaze = dicom["00220006"]["Value"][0]["00080100"]["Value"][0]
        else:
            gaze = "N/A"

        framenumber = referencedsopinstance = slicethickness = "N/A"
    # B-Scan OCT
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.4":
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        laterality = dicom["00200062"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        framenumber = dicom["00280008"]["Value"][0]
        softwareversion = dicom["00181020"]["Value"][0]
        numberoffiles = filecount
        referencedsopinstance = dicom["52009229"]["Value"][0]["00081140"]["Value"][0][
            "00081155"
        ]["Value"][0]
        if (
            "52009229" in dicom
            and "00289110" in dicom["52009229"]["Value"][0]
            and "00180050" in dicom["52009229"]["Value"][0]["00289110"]["Value"][0]
        ):
            slicethickness = dicom["52009229"]["Value"][0]["00289110"]["Value"][0][
                "00180050"
            ]["Value"][0]
        else:
            slicethickness = ""

        privatetag = gaze = "N/A"

    # B-scan Volume Analysis Storage
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.8":
        laterality = dicom["52009229"]["Value"][0]["00209071"]["Value"][0]["00209072"][
            "Value"
        ][0]
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        framenumber = dicom["00280008"]["Value"][0]
        device = dicom["00081090"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        slicethickness = dicom["52009229"]["Value"][0]["00289110"]["Value"][0][
            "00180050"
        ]["Value"][0]
        referencedsopinstance = dicom["00200052"]["Value"][0]
        privatetag = softwareversion = gaze = "N/A"
        numberoffiles = filecount

    # segmentation
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.66.5":
        laterality = dicom["00200062"]["Value"][0]
        device = dicom["00081090"]["Value"][0]
        referencedsopinstance = dicom["00081115"]["Value"][0]["0008114A"]["Value"][0][
            "00081155"
        ]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        numberoffiles = filecount
        rows = (
            columns
        ) = framenumber = slicethickness = privatetag = gaze = softwareversion = "N/A"

    # en face
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.7":  # en face
        laterality = dicom["00200062"]["Value"][0]
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        numberoffiles = filecount
        referencedsopinstance = dicom["00082112"]["Value"][0]["00081155"]["Value"][0]
        framenumber = slicethickness = privatetag = gaze = softwareversion = "N/A"

    # unknown
    else:
        sopinstanceuid = f"Unknown SOP Class UID: {sopclassuid}"
        laterality = (
            device
        ) = (
            rows
        ) = (
            referencedsopinstance
        ) = (
            implementationversion
        ) = (
            columns
        ) = (
            framenumber
        ) = slicethickness = privatetag = gaze = numberoffiles = softwareversion = "N/A"

    output = DicomEntry(
        filename,
        patientid,
        sopclassuid,
        sopinstanceuid,
        laterality,
        rows,
        columns,
        device,
        framenumber,
        referencedsopinstance,
        slicethickness,
        implementationversion,
        gaze,
        privatetag,
        softwareversion,
        numberoffiles,
    )
    return output


def find_rule(file):
    dicomentry = extract_dicom_entry(file)
    matching_rules = [rule for rule in rules if rule.apply(dicomentry)]
    if matching_rules:
        for rule in matching_rules:
            return str(rule.name)
    else:
        return "No rules apply."


## Domain, Modality, Protocol, Patient ID, Laterlity, sopinstanceuid, referencedsopinstance
def extract_dicom_summary(file):
    dicomentry = extract_dicom_entry(file)
    sopclassuid = dicomentry.sopclassuid

    try:
        dcm = pydicom.dcmread(file)
        domain = "DICOM"

    except pydicom.errors.InvalidDicomError:
        domain = "NOT DICOM"

    if sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.1":
        modality = "CFP/IR/FAF"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.4":
        modality = "OCT B Scan"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.8":
        modality = "B-scan Volume Analysis Storage"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.66.5":
        modality = "Surface Segmentation Storage"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.7":
        modality = "En Face OCTA Image"
    else:
        modality = sopclassuid

    sopinstanceuid = dicomentry.sopinstanceuid
    device = dicomentry.device
    patientid = dicomentry.patientid
    laterality = dicomentry.laterality
    referencedsopinstance = dicomentry.referencedsopinstance
    softwareversion = dicomentry.softwareversion
    numberoffiles = dicomentry.numberoffiles
    protocol = find_rule(file)

    output = DicomSummary(domain, patientid, laterality, protocol)
    return output


def get_dicom_summary(file):
    dicomsummary = extract_dicom_summary(file)
    obj_dict = vars(dicomsummary)
    return obj_dict


def list_files_recursive(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            all_files.append(file_path)
    return all_files


def process_dicom_zip(zip_file_path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            extracted_files = list_files_recursive(temp_dir)

            dicom_files = [
                f for f in extracted_files if f.endswith(".dcm") and "/__" not in f
            ]

            if len(dicom_files) == 1:
                dicom_file_path = os.path.join(temp_dir, dicom_files[0])
                dicom = get_dicom_summary(dicom_file_path)
                return dicom

            elif len(dicom_files) > 1:
                for dicom_file in dicom_files:
                    if dicom_file.endswith(".1.1.dcm") and "/." not in dicom_file:
                        dicom_file_path = os.path.join(temp_dir, dicom_file)
                        dicom = get_dicom_summary(dicom_file_path)
                        return dicom
            else:
                print("Error: no DICOM file present in the zip archive.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    return None


def process_env_zip(file_path):
    path_parts = file_path.split("/")
    filename = path_parts[-1]
    filename_parts = filename.split("-")
    patient_id = "AIREADI-" + filename_parts[-2]
    sensor_id = filename_parts[-1].split(".")[0]
    info_dict = {
        "domain": "CSV",
        "patient_id": patient_id,
        "laterality": "N/A",
        "protocol": "environmental_sensor",
        "sensor_id": sensor_id,
    }

    return info_dict


def process_flio_zip(file_path):
    path_parts = file_path.split("/")
    filename = path_parts[-1]
    filename_parts = filename.split("_")
    patient_id = "AIREADI-" + filename_parts[-7]
    laterality = filename_parts[-1][:2]

    if laterality == "OD":
        laterality = "R"

    elif laterality == "OS":
        laterality = "L"
    else:
        print("Invalid laterality")

    info_dict = {
        "domain": "DICOM",
        "patient_id": patient_id,
        "laterality": laterality,
        "protocol": "FLIO",
    }
    return info_dict


def process_ecg_zip(zip_file_path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            extracted_files = list_files_recursive(temp_dir)

            ecg_file = [f for f in extracted_files][0]
            xdom = minidom.parse(ecg_file)
            content = xdom.documentElement.toxml()  # a very long string!
            my_dict = xmltodict.parse(content)
            restingecg = my_dict["restingecgdata"]

            # 4 key items
            key_items = dict()
            key_items["domain"] = "xml"
            key_items["laterality"] = "NA"
            key_items["protocol"] = "ECG"
            key_items["docname"] = restingecg["documentinfo"]["documentname"]
            key_items["pos"] = my_dict["restingecgdata"]["userdefines"]["userdefine"][
                0
            ]["value"]
            key_items["patientid"] = my_dict["restingecgdata"]["patient"][
                "generalpatientdata"
            ]["name"]["firstname"]
            return key_items

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    return None
