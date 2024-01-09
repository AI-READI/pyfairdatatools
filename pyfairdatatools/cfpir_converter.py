import os
import shutil
import tempfile
import zipfile

import pydicom

KEEP = 0
BLANK = 1
HARMONIZE = 2


class ConversionRule:
    """
    Represents a conversion rule for processing data.

    This class defines a rule used for data conversion and processing. It contains attributes
    such as the rule's name, header elements, individual elements, and sequences of elements.

    Attributes:
        name (str): The name of the conversion rule.
        header_elements (list): List of Element instances representing header elements.
        elements (list): List of Element instances representing individual elements.
        sequences (list): List of Sequence instances representing sequences of elements.

    Methods:
        header_tags(): Extracts unique tags from header elements.
        tags(): Extracts unique tags from individual elements.
        sequence_tags(): Generates a dictionary of sequence tags and associated element tags.

    """

    def __init__(self, name, headers, elements, sequences):
        self.name = name
        self.header_elements = headers
        self.elements = elements
        self.sequences = sequences

    def header_tags(self):
        headertags = set()
        for header_element in self.header_elements:
            headertags.add(header_element.tag)

        return list(headertags)

    def tags(self):
        tags = set()
        for element in self.elements:
            tags.add(element.tag)

        return list(tags)

    def sequence_tags(self):
        tags_dict = {}
        for sequence in self.sequences:
            element_tags = [element.tag for element in sequence.elements]
            tags_dict[sequence.tag] = element_tags

        return tags_dict


class Element:
    """
    Represents an individual data element.

    This class defines an individual data element with attributes such as its name, tag,
    value representation (vr), decision, and harmonized value.

    Attributes:
        name (str): The name of the data element.
        tag (str): The tag associated with the data element.
        vr (str): The value representation of the data element.
        decision (int): The decision related to the data element (default is 0).
        harmonized_value (int): The harmonized value of the data element (default is 0).
    """

    def __init__(self, name, tag, vr, decision=0, harmonized_value=0):
        self.name = name
        self.tag = tag
        self.vr = vr
        self.decision = decision
        self.harmonized_value = harmonized_value


class ElementList:
    """
    Represents a list of related data elements.

    This class defines a list of related data elements with attributes such as its name,
    tag, value representation (vr), and the list of elements.

    Attributes:
        name (str): The name of the element list.
        tag (str): The tag associated with the element list.
        vr (str): The value representation of the element list.
        elements (list): List of Element instances representing the data elements in the list (default is an empty list).
    """

    def __init__(self, name, tag, vr, elements=None):
        self.name = name
        self.tag = tag
        self.vr = vr
        self.elements = elements if elements is not None else []


cfp_ir = ConversionRule(
    "CFP IR",
    # DICOM header elements
    headers=[
        Element("FileMetaInformationGroupLength", "00020000", "UL"),
        Element("FileMetaInformationVersion", "00020001", "OB"),
        Element("MediaStorageSOPClassUID", "00020002", "UI"),
        Element("MediaStorageSOPInstanceUID", "00020003", "UI"),
        Element("TransferSyntaxUID", "00020010", "UI"),
        Element("ImplementationClassUID", "00020012", "UI"),
        Element("ImplementationVersionName", "00020013", "SH"),
    ],
    # DICOM elements
    elements=[
        Element("PatientName", "00100010", "PN", BLANK),
        Element("PatientID", "00100020", "LO"),
        Element("PatientBirthDate", "00100030", "DA", BLANK),
        Element("PatientSex", "00100040", "CS", BLANK),
        Element("StudyInstanceUID", "0020000D", "UI"),
        Element("StudyDate", "00080020", "DM"),
        Element("StudyTime", "00080030", "TM"),
        Element("ReferringPhysicianName", "00080090", "PN", BLANK),
        Element("StudyID", "00200010", "SH", BLANK),
        Element("AccessionNumber", "00080050", "SH", BLANK),
        Element("StudyDescription", "00081030", "LO", HARMONIZE, "CFP/IR"),
        Element("Modality", "00080060", "CS"),
        Element("SeriesInstanceUID", "0020000E", "UI"),
        Element("SeriesNumber", "00200011", "IS"),
        Element("SynchronizationFrameOfReferenceUID", "00200200", "UI"),
        Element("SynchronizationTrigger", "0018106A", "CS"),
        Element("AcquisitionTimeSynchronized", "00181800", "CS"),
        Element("Manufacturer", "00080070", "LO"),
        Element("ManufacturerModelName", "00081090", "LO"),
        Element("DeviceSerialNumber", "00181000", "LO"),
        Element("SoftwareVersions", "00181020", "LO"),
        Element("InstanceNumber", "00200013", "IS"),
        Element("PatientOrientation", "00200020", "CS"),
        Element("BurnedInAnnotation", "00280301", "CS"),
        Element("PatientEyeMovementCommanded", "00220005", "CS"),
        Element("HorizontalFieldOfView", "0022000C", "FL"),
        Element("DetectorType", "00187004", "CS"),
        Element("Rows", "00280010", "US"),
        Element("Columns", "00280011", "US"),
        Element("BitsAllocated", "00280100", "US"),
        Element("BitsStored", "00280101", "US"),
        Element("HighBit", "00280102", "US"),
        Element("PixelRepresentation", "00280103", "US"),
        Element("SamplePerPixel", "00280002", "US"),
        Element("PlanarConfiguration", "00280006", "US"),
        Element("PhotometricInterpretation", "00280004", "CS"),
        Element("NumberOfFrames", "00280008", "IS"),
        Element("FrameIncrementPointer", "00280009", "AT"),
        Element("ImageType", "00080008", "CS", HARMONIZE, "ORIGINAL PRIMARY"),
        Element("ContentTime", "00080033", "TM"),
        Element("ContentDate", "00080023", "DA"),
        Element("AcquisitionDateTime", "0008002A", "DT"),
        Element("LossyImageCompression", "00282110", "CS"),
        Element("LossyImageCompressionRatio", "00282112", "DS"),
        Element("LossyImageCompressionMethod", "00282114", "CS"),
        Element("PresentationLUTShape", "20500020", "CS"),
        Element("PixelSpacing", "00280030", "DS"),
        Element("ImageLaterality", "00200062", "CS"),
        Element("PatientEyeMovementCommanded", "00220005", "CS"),
        Element("HorizontalFieldOfView", "0022000C", "FL"),
        Element("DetectorType", "00187004", "CS"),
        Element("SOPClassUID", "00080016", "UI"),
        Element("SOPInstanceUID", "00080018", "UI"),
        Element("SpecificCharacterSet", "00080005", "CS"),
    ],
    # DICOM sequences
    sequences=[
        ElementList("LightPathFilterTypeStackCodeSequence", "00220017", "SQ"),
        ElementList("ImagePathFilterTypeStackCodeSequence", "00220018", "SQ"),
        ElementList(
            "LensesCodeSequence",
            "00220019",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH"),
                Element("CodingSchemeDesignator", "00080102", "SH"),
                Element("CodeMeaning", "00080104", "LO"),
            ],
        ),
        ElementList(
            "IlluminationTypeCodeSequence",
            "00220016",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH"),
                Element("CodingSchemeDesignator", "00080102", "SH"),
                Element("CodeMeaning", "00080104", "LO"),
            ],
        ),
        ElementList(
            "ChannelDescriptionCodeSequence",
            "0022001A",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH"),
                Element("CodingSchemeDesignator", "00080102", "SH"),
                Element("CodeMeaning", "00080104", "LO"),
            ],
        ),
        ElementList(
            "PatientEyeMovementCommandCodeSequence",
            "00220006",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH"),
                Element("CodingSchemeDesignator", "00080102", "SH"),
                Element("CodeMeaning", "00080104", "LO"),
            ],
        ),
        ElementList(
            "AnatomicRegionSequence",
            "00082218",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH", HARMONIZE, "T-AA610"),
                Element("CodingSchemeDesignator", "00080102", "SH", HARMONIZE, "SRT"),
                Element("CodeMeaning", "00080104", "LO", HARMONIZE, "Retina"),
            ],
        ),
        ElementList(
            "AcquisitionDeviceTypeCodeSequence",
            "00220015",
            "SQ",
            [
                Element("CodeValue", "00080100", "SH"),
                Element("CodingSchemeDesignator", "00080102", "SH"),
                Element("CodeMeaning", "00080104", "LO"),
            ],
        ),
    ],
)


def process_tags(tags, dicom):
    """
    Process DICOM tags and create a dictionary of DicomEntry instances.

    This function processes a list of DICOM tags from a given DICOM dictionary and constructs
    a dictionary of DicomEntry instances representing the metadata associated with each tag.

    Args:
        tags (list): List of DICOM tags to process.
        dicom (dict): The DICOM dictionary containing the metadata.

    Returns:
        dict: Dictionary where keys are DICOM tags and values are DicomEntry instances.

    """
    output = dict()
    for tag in tags:
        if tag in dicom:
            element_name = pydicom.tag.Tag(tag)
            vr = dicom[tag]["vr"]
            value = dicom[tag].get(
                "Value", []
            )  # Assign [] as value if "Value" key is not present

            if not value or not isinstance(value[0], dict):
                output[tag] = DicomEntry(tag, element_name, vr, value)
            else:
                data = dicom[tag]["Value"][0]
                keys_list = list(data.keys())
                nested_output = process_tags(keys_list, data)
                output[tag] = DicomEntry(tag, element_name, vr, [nested_output])
    return output


class DicomEntry:
    """
    Represents a DICOM metadata entry.

    This class encapsulates information about a single DICOM metadata entry, including its
    tag, name, value representation (vr), and associated value.

    Attributes:
        tag (str): The DICOM tag of the metadata entry.
        name (pydicom.tag.Tag): The name (tag) associated with the metadata entry.
        vr (str): The value representation of the metadata entry.
        value (list): The value associated with the metadata entry.

    Methods:
        is_empty(): Checks if the value of the metadata entry is empty.

    """

    def __init__(self, tag, name, vr, value):
        self.tag = tag
        self.name = name
        self.vr = vr
        self.value = value

    def is_empty(self):
        return len(self.value) == 0


def extract_dicom_dict(file, tags):
    """
    Extract DICOM metadata and information from a DICOM file.

    This function reads a DICOM file, extracts metadata, header elements, and specific
    tags from it. It then processes the tags to create a dictionary representation of
    the DICOM metadata, along with information about transfer syntax and pixel data.

    Args:
        file (str): The path to the DICOM file.
        tags (list): List of DICOM tags to process.

    Returns:
        tuple: A tuple containing:
            - dict: Dictionary representation of DICOM metadata with processed tags.
            - list: List of transfer syntax information.
            - bytes: Pixel data from the DICOM file.

    Raises:
        FileNotFoundError: If the specified DICOM file does not exist.

    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found.")

    output = dict()
    output["filepath"] = file

    dataset = pydicom.dcmread(file)

    header_elements = {
        "00020000": {
            "vr": "UL",
            "Value": [dataset.file_meta.FileMetaInformationGroupLength],
        },
        "00020001": {
            "vr": "OB",
            "Value": [dataset.file_meta.FileMetaInformationVersion],
        },
        "00020002": {"vr": "UI", "Value": [dataset.file_meta.MediaStorageSOPClassUID]},
        "00020003": {
            "vr": "UI",
            "Value": [dataset.file_meta.MediaStorageSOPInstanceUID],
        },
        "00020010": {
            "vr": "UI",
            "Value": [dataset.file_meta.TransferSyntaxUID],
        },
        "00020012": {
            "vr": "UI",
            "Value": [dataset.file_meta.ImplementationClassUID],
        },
        "00020013": {
            "vr": "SH",
            "Value": [dataset.file_meta.ImplementationVersionName],
        },
    }
    json_dict = {}
    json_dict.update(header_elements)
    info = dataset.to_json_dict()

    patient_name = dataset.PatientName
    info["00100010"]["Value"] = [patient_name]

    physician_name = dataset.ReferringPhysicianName
    info["00080090"]["Value"] = [physician_name]

    json_dict.update(info)

    dicom = json_dict

    output = process_tags(tags, dicom)

    transfersyntax = [dataset.is_little_endian, dataset.is_implicit_VR]
    pixeldata = dataset.PixelData

    return output, transfersyntax, pixeldata


def write_dicom(protocol, dicom_dict_list, file_path):
    """
    Write DICOM data to a new DICOM file.

    This function takes a protocol, a list of DICOM dictionaries, and a file path. It constructs
    a new DICOM dataset using the provided protocol and DICOM dictionaries. The dataset is then
    written to a new DICOM file at the specified path.

    Args:
        protocol (ConversionRule): The ConversionRule instance containing processing instructions.
        dicom_dict_list (list): List containing DICOM dictionaries and related information.
        file_path (str): The path to the new DICOM file to be created.

    """
    headertags = protocol.header_tags()
    tags = protocol.tags()
    sequencetags = protocol.sequence_tags()

    file_meta = pydicom.Dataset()

    for headertag in headertags:
        value = dicom_dict_list[0][headertag].value
        element_name = pydicom.datadict.keyword_for_tag(
            dicom_dict_list[0][headertag].tag
        )
        setattr(file_meta, element_name, value)

    dataset = pydicom.Dataset()
    dataset.file_meta = file_meta

    for tag in tags:
        for element in protocol.elements:
            if element.tag == tag:
                desired_element = element

        if desired_element.decision == BLANK:
            value = []

        elif desired_element.decision == HARMONIZE:
            value = [desired_element.harmonized_value]

        elif tag in dicom_dict_list[0]:
            value = dicom_dict_list[0][tag].value

        else:
            value = []

        element_name = (
            pydicom.datadict.keyword_for_tag(dicom_dict_list[0][tag].tag)
            if tag in dicom_dict_list[0]
            else pydicom.datadict.keyword_for_tag(tag)
        )
        setattr(dataset, element_name, value)

    dataset.is_little_endian = dicom_dict_list[1][0]
    dataset.is_implicit_VR = dicom_dict_list[1][1]
    dataset.PixelData = dicom_dict_list[2]

    if dicom_dict_list[0]["00081090"].value == ["Triton"]:
        dataset.Manufacturer = ["Topcon"]

    keys = list(sequencetags.keys())

    for key in keys:
        for sequence in protocol.sequences:
            if sequence.tag == key:
                desired_sequence = sequence

        if key in dicom_dict_list[0]:
            sequencetag = key
            seq = pydicom.Sequence()
            elementkeys = sequencetags[sequencetag]

            if dicom_dict_list[0][key].value:
                x = dicom_dict_list[0][key].value[0]
                key_list = list(x.keys())

                item = pydicom.Dataset()
                for elementkey in elementkeys:
                    for element in desired_sequence.elements:
                        if element.tag == elementkey:
                            desired_element = element
                    if elementkey in key_list and desired_element.decision == BLANK:
                        value = []
                    elif (
                        elementkey in key_list and desired_element.decision == HARMONIZE
                    ):
                        value = desired_element.harmonized_value
                    elif elementkey in key_list:
                        value = dicom_dict_list[0][key].value[0][elementkey].value
                    element_tag = (
                        dicom_dict_list[0][sequencetag].value[0][elementkey].tag
                    )
                    element_name = pydicom.datadict.keyword_for_tag(element_tag)
                    setattr(item, element_name, value)
                seq.append(item)

                value = seq
                element_name = pydicom.datadict.keyword_for_tag(
                    dicom_dict_list[0][key].tag
                )
                setattr(dataset, element_name, value)

            else:
                value = seq
                element_name = pydicom.datadict.keyword_for_tag(
                    dicom_dict_list[0][key].tag
                )
                setattr(dataset, element_name, value)
        else:
            value = pydicom.Sequence()
            element_name = pydicom.datadict.keyword_for_tag(key)
            setattr(dataset, element_name, value)
    pydicom.filewriter.write_file(file_path, dataset, write_like_original=False)


def convert_dicom(input, output):
    """
    Convert DICOM data from an input file to an output file using a conversion rule.

    This function facilitates the conversion of DICOM data from an input file to an output file.
    It uses a specified conversion rule to process the data and writes the converted data to the
    output file.

    Args:
        input (str): The path to the input DICOM file.
        output (str): The path to the output DICOM file to be created.

    """
    conversion_rule = cfp_ir
    tags = (
        conversion_rule.header_tags()
        + conversion_rule.tags()
        + list(conversion_rule.sequence_tags().keys())
    )
    x = extract_dicom_dict(input, tags)
    write_dicom(conversion_rule, x, output)


def list_files_recursive(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            all_files.append(file_path)
    return all_files


def convert_zip_dicom(zip_file_path, output):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            extracted_files = list_files_recursive(temp_dir)
            convert_dicom(extracted_files[0], output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    return None
