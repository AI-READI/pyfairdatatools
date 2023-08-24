import os

import pydicom


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
        "Eidom_UWF_Central_IR",
        conditions=[
            lambda entry: "0-infrared" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    ClassifyingRule(
        "Eidom_UWF_Central_FAF",
        conditions=[
            lambda entry: "0-af" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    ClassifyingRule(
        "Eidom_UWF_Central_CFP",
        conditions=[
            lambda entry: "0-visible" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    ClassifyingRule(
        "Eidom_UWF_Nasal_CFP",
        conditions=[
            lambda entry: "3-visible" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    ClassifyingRule(
        "Eidom_UWF_Temporal_CFP",
        conditions=[
            lambda entry: "4-visible" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    ClassifyingRule(
        "Eidom_UWF_Mosaic_CFP",
        conditions=[
            lambda entry: "11-visible" in entry.filename.lower()
            and "Eidon FA" == entry.device
        ],
    ),
    # maestro
    ClassifyingRule(
        "Maestro2_3D_Wide_OCT",
        conditions=[
            lambda entry: "3DOCT-1Maestro2" == entry.device
            and "IMAGENET6V2_1" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and "0.07086614173" == str(entry.slicethickness)
        ],
    ),
    ClassifyingRule(
        "Maestro2_3D_Macula_OCT",
        conditions=[
            lambda entry: "3DOCT-1Maestro2" == entry.device
            and "IMAGENET6V2_1" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and "0.04724409449" == str(entry.slicethickness)
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCT_reference_CFP",
        conditions=[
            lambda entry: "3DOCT-1Maestro2" == entry.device
            and "IMAGENET6V2_1" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.1" == entry.sopclassuid
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_reference_Bscan",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_reference_CFP",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".2.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_Segmentation",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".4.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_volumeanalysis_unprocessed",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".3.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_volumeanalysis_for_presentation",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".5.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_enface_superficial",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.3.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_enface_deep",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.4.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_enface_choriocapillaris",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.5.dcm")
        ],
    ),
    ClassifyingRule(
        "Maestro2_OCTA_enface_outer_retina",
        conditions=[
            lambda entry: entry.device == "3DOCT-1Maestro2"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.80.dcm")
        ],
    ),
    # triton
    ClassifyingRule(
        "Triton_3D(H)_Radial_OCT",
        conditions=[
            lambda entry: "TP_STO_IM6_100" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.4" == entry.sopclassuid
            and "Triton" == entry.device
        ],
    ),
    ClassifyingRule(
        "Triton_3D(H)_Radial_OCT_reference_CFP",
        conditions=[
            lambda entry: "TP_STO_IM6_100" == entry.implementationversion
            and "1.2.840.10008.5.1.4.1.1.77.1.5.1" == entry.sopclassuid
            and "Triton" == entry.device
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_reference_Bscan",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.01875"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_reference_CFP",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".2.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_Segmentation",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.01875"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".4.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_volumeanalysis_unprocessed",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.01875"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".3.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_volumeanalysis_for_presentation",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.01875"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".5.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_enface_superficial",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.3.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_enface_deep",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.4.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_enface_choriocapillaris",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.5.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_6*6_OCTA_enface_outer_retina",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.80.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_reference_Bscan",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.0234375"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".1.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_reference_CFP",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".2.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_Segmentation",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".4.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_volumeanalysis_unprocessed",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.0234375"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".3.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_volumeanalysis_for_presentation",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and str(entry.slicethickness) == "0.0234375"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".5.1.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_enface_superficial",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.3.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_enface_deep",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.4.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_enface_choriocapillaris",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.5.dcm")
        ],
    ),
    ClassifyingRule(
        "Triton_Macula_12*12_OCTA_enface_outer_retina",
        conditions=[
            lambda entry: entry.device == "Triton plus"
            and "fo-dicom 4.0.8" == entry.implementationversion
            and entry.filename.startswith("2.16.840.1.114517.10.1.1.4.")
            and entry.filename.endswith(".6.80.dcm")
        ],
    ),
    # #spectralis
    ClassifyingRule(
        "Spec_ONH_RC_HR_OCT",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.framenumber) == "27"
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
            and str(entry.framenumber) == "61"
            and str(entry.rows) == "496"
            and str(entry.columns) == "768"
            and entry.slicethickness != ""
        ],
    ),
    ClassifyingRule(
        "Spec_PPole_Mac_HR_OCT_reference_IR",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.rows) == "768"
            and str(entry.columns) == "768"
            and str(entry.privatetag) == "N/A"
        ],
    ),
    ClassifyingRule(
        "Spec-Mac-20x20-HS_OCTA_reference_Bscan",
        conditions=[
            lambda entry: entry.device == "Spectralis"
            and str(entry.framenumber) == "512"
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
    ),
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
        privatetag,
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
        self.privatetag = privatetag


class DicomSummary:
    def __init__(
        self, domain, modality, device, patientid, laterality, description
    ):  # sopinstance, matchingcfpifsopinstance
        self.domain = domain  # DICOM
        self.modality = modality  # CFP, IR, OCT B scan, ...
        self.device = device  # Device name
        self.patientid = patientid  # patient id
        self.laterality = laterality  # laterality
        self.description = description  # belongs to which one in AIREADI checklist


def extract_dicom_entry(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found.")

    dicom = pydicom.dcmread(file).to_json_dict()
    ds = pydicom.dcmread(file)

    filename = os.path.basename(file)
    patientid = dicom["00100020"]["Value"][0]
    sopclassuid = dicom["00080016"]["Value"][0]
    sopinstanceuid = dicom["00080018"]["Value"][0]

    if sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.1":
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        laterality = dicom["00200062"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        # Check if privatetag value exists
        if "00511017" in dicom:
            privatetag = dicom["00511017"]["Value"][0]
        else:
            privatetag = "N/A"
        framenumber = referencedsopinstance = slicethickness = "N/A"

    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.4":
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        laterality = dicom["00200062"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        framenumber = dicom["00280008"]["Value"][0]
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
        privatetag = "N/A"

    elif (
        sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.8"
    ):  # B-scan Volume Analysis Storage
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
        privatetag = "N/A"

    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.66.5":
        laterality = dicom["00200062"]["Value"][0]
        device = dicom["00081090"]["Value"][0]
        referencedsopinstance = dicom["00081115"]["Value"][0]["0008114A"]["Value"][0][
            "00081155"
        ]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        rows = columns = framenumber = slicethickness = privatetag = "N/A"

    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.7":  # en face
        laterality = dicom["00200062"]["Value"][0]
        rows = dicom["00280010"]["Value"][0]
        columns = dicom["00280011"]["Value"][0]
        implementationversion = ds.file_meta.ImplementationVersionName
        device = dicom["00081090"]["Value"][0]
        referencedsopinstance = dicom["00082112"]["Value"][0]["00081155"]["Value"][0]
        framenumber = slicethickness = privatetag = "N/A"

    else:  # unknown
        sopinstanceuid = f"Unknown SOP Class UID: {sopclassuid}"
        laterality = (
            device
        ) = (
            rows
        ) = (
            referencedsopinstance
        ) = (
            implementationversion
        ) = columns = framenumber = slicethickness = privatetag = "N/A"

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
        privatetag,
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


def extract_dicom_summary(file):
    dicomentry = extract_dicom_entry(file)
    sopclassuid = dicomentry.sopclassuid

    try:
        dcm = pydicom.dcmread(file)
        domain = "DICOM"

    except pydicom.errors.InvalidDicomError:
        domain = "NOT DICOM"

    if sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.1":
        modality = "CFP/IR"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.4":
        modality = "OCT B Scan"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.8":
        modality = "B-scan Volume Analysis Storage"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.66.5":
        modality = "Surface Segmentation Storage"
    elif sopclassuid == "1.2.840.10008.5.1.4.1.1.77.1.5.7":
        modality = "En Face OCTA Image"

    device = dicomentry.device
    patientid = dicomentry.patientid
    laterality = dicomentry.laterality
    referencedsopinstance = dicomentry.referencedsopinstance
    description = find_rule(file)

    output = DicomSummary(domain, modality, device, patientid, laterality, description)
    return output


def get_dicom_summary(file):
    dicomsummary = extract_dicom_summary(file)
    obj_dict = vars(dicomsummary)
    return obj_dict


def is_dicom_file(file_path):
    try:
        pydicom.dcmread(file_path)
        return True
    except pydicom.errors.InvalidDicomError:
        return False
