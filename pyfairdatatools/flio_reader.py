import struct

import matplotlib.pyplot as plt
import numpy as np


class Module:
    def __init__(self, name, elements):
        """
        Initialize a Module with a name and a list of elements.

        Args:
            name (str): The name of the module.
            elements (list): A list of elements within the module.
        """
        self.name = name
        self.elements = elements

    def calculate_total_length(self):
        """
        Calculate the total length of all elements in the module.

        Returns:
            int: The sum of lengths of all elements.
        """
        total_length = 0
        for element in self.elements:
            total_length += element.length
        return total_length


# Length is in byte
class Element:
    def __init__(self, name, datatype, length):
        """
        Initialize an Element with its properties.

        Args:
            name (str): The name of the element.
            datatype (str): The data type of the element.
            length (int): The length of the element.
        """
        self.name = name
        self.datatype = datatype
        self.length = length


flioheader = Module(
    "File Header",
    [  # software revision number
        Element("revision", "short", 2),
        # offset of the info part which contians general information
        Element("info_offset", "long", 4),
        # length of the info part
        Element("info_length", "short", 2),
        # offset of the setup data
        Element("setup_offs", "long", 4),
        # length of the setup data
        Element("setup_length", "short", 2),
        # length of the setup data
        Element("data_block_offset", "long", 4),
        # offset of the first data block
        Element("no_of_data_blocks", "short", 2),
        # number of data blocks valid only when 0.. 0x7ffe range
        Element("data_block_length", "long", 4),
        # length of the longest data block in the file
        Element("meas_desc_block_offset", "long", 4),
        # offset to 1st measurement description block
        Element("no_of_meas_desc_blocks", "short", 2),
        # number of measurement description blocks
        Element("meas_desc_block_length", "short", 2),
        # valid: 0x5555, not valid 0x1111
        Element("header_valid", "unsigned short", 2),
        # reserved1 reserved 1 now contains no_of_data_blocks
        Element("reserved1", "unsigned long", 4),
        # reserved2
        Element("reserved2", "unsigned short", 2),
        # checksum of file header
        Element("chksum", "unsigned short", 2),
    ],
)

fliomeasurement = Module(
    "Measurement Description Blocks",
    [  # time of creation
        Element("time", "char", 9),
        # date of creation
        Element("date", "char", 11),
        # serial number
        Element("mod_ser_no", "char", 16),
        # model serial number
        Element("measurement mode", "short", 2),
        # CFD_LL (Constant Fraction Discriminator - Lower Level)
        Element("cfd_ll", "float", 4),
        # CFD_LH (Constant Fraction Discriminator - Upper Level)
        Element("cfd_lh", "float", 4),
        # CFD_ZC (Constant Fraction Discriminator - Zero Crossing):
        Element("cfd_zc", "float", 4),
        # CFD_HF (Constant Fraction Discriminator - High Frequency)
        Element("cfd_hf", "float", 4),
        # SYN_ZC (Synchronization - Zero Crossing)
        Element("syn_zc", "float", 4),
        # SYN_FD (Synchronization - Fast Detector)
        Element("syn_fd", "float", 4),
        # SYN_HF (Synchronization - High Frequency)
        Element("syn_hf", "float", 4),
        # TAC_R (Time-to-Amplitude Converter - Reference Channel)
        Element("tac_r", "float", 4),
        # TAC_G (Time-to-Amplitude Converter - Gate Channel)
        Element("tac_g", "float", 4),
        #
        Element("tac_of", "float", 4),
        # AC_LL (Time-to-Amplitude Converter - Lower Level)
        Element("tac_ll", "float", 4),
        #  Time-to-Amplitude Converter - Upper Level
        Element("tac_lh", "float", 4),
        # Analog-to-Digital Converter - Resolution
        Element("adc_re", "short", 2),
        # Emission Wavelength - Delay
        Element("eal_de", "short", 2),
        # Number of Columns and Rows
        Element("ncx", "short", 2),
        # Number of Columns and Rows
        Element("ncy", "short", 2),
        # Page Number
        Element("page", "unsigned short", 2),
        # Page Number
        Element("col_t", "float", 4),
        # Repetition Time
        Element("rep_t", "float", 4),
        #  Stop Time
        Element("stopt", "short", 2),
        # Overflow
        Element("overfl", "char", 9),
        # Use Motor
        Element("use_motor", "short", 2),
        # Steps
        Element("steps", "short", 2),
        # Offset
        Element("offset", "float", 4),
        # Dithering
        Element("dither", "short", 2),
        # Increment
        Element("incr", "short", 2),
        # Memory Bank
        Element("mem_bank", "short", 2),
        # Module Type
        Element("module type", "char", 16),
        # Synthesis Threshold
        Element("syn_th", "float", 4),
        # Dead Time Compensation
        Element("dead_time_comp", "short", 2),
        # Polarity
        Element("polarity_l", "short", 2),
        # Polarity
        Element("polarity_f", "short", 2),
        # Polarity
        Element("polarity_p", "short", 2),
        # Line Division
        Element("linediv", "short", 2),
        # Accumulation
        Element("accumulate", "short", 2),
        # Flyback Y
        Element("flbck_y", "int", 2),
        # Flyback X
        Element("flbck_x", "int", 2),
        # Border Upper
        Element("bord_u", "int", 2),
        # Border Lower
        Element("bord_l", "int", 2),
        # Pixel Time
        Element("pix_time", "float", 4),
        # Pixel Clock
        Element("pix_clk", "short", 2),
        # Trigger
        Element("trigger", "short", 2),
        # Scan x
        Element("scan_x", "int", 2),
        # Scan y
        Element("scan_y", "int", 2),
        # Scan range x
        Element("scan_rx", "int", 2),
        # Scan range y
        Element("scan_ry", "int", 2),
        # First In First Out
        Element("fifo_typ", "short", 2),
        # Epixel Division
        Element("epx_div", "int", 2),
        # Module Type Code
        Element("mod_type_code", "int", 2),
        # Overflow Correction Factor
        Element("overflow_corr_factor", "float", 4),
        # ADC Zoom
        Element("adc_zoom", "int", 2),
        # Cycles
        Element("cycles", "int", 2),
    ],
)

datablock = Module(
    "Data Blocks",
    [  # block_no
        Element("block number", "short", 2),
        # data_offs
        Element("data offs", "long", 4),
        # next_block_offs
        Element("next block offs", "long", 4),
        # block_type
        Element("block type", "unsigned short", 2),
        # meas_desc_block_no
        Element("meas_desc_block_no", "short", 2),
        # lblock_no
        Element("lblock_no", "unsigned long", 4),
        # block_length
        Element("block_length", "long", 4),
        # image
        Element("image", "", 134217728),
    ],
)


def file_information(file_path):
    """
    Extract relevant information from a binary file.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        dict: A dictionary containing extracted information.
    """
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Find the start and end indexes of the relevant section
    start_index = file_content.find(b"*IDENTIFICATION")
    end_index = file_content.find(b"*END", start_index)

    extracted_info = {}

    if start_index != -1 and end_index != -1:
        relevant_content = file_content[start_index:end_index]

        # Split the content into lines
        lines = relevant_content.split(b"\n")

        # Labels to search for (as bytes)
        labels_to_find = [
            b"ID",
            b"Title",
            b"Version",
            b"Revision",
            b"Date",
            b"Time",
            b"Author",
            b"Company",
            b"Contents",
        ]
        for line in lines:
            for label in labels_to_find:
                if line.startswith(label):
                    value = line[len(label) :].strip()
                    extracted_info[label.decode("utf-8")] = value.decode("utf-8")
                    break

    return extracted_info


def read_element(file, data_type, size, byte_order="little"):
    """
    Read and convert data from a binary file based on the specified data type.

    Args:
        file (file object): The binary file object.
        data_type (str): The data type to read and convert.
        size (int): The size of the data to read, in bytes.
        byte_order (str): The byte order for reading numeric data. Defaults to "little".

    Returns:
        The read and converted data, or appropriate value based on the data type.
    """
    if data_type == "short":
        return int.from_bytes(file.read(size), byteorder="little", signed=True)
    elif data_type == "char":
        return file.read(size)
    elif data_type == "long":
        return int.from_bytes(file.read(size), byteorder="little", signed=True)
    elif data_type == "unsigned short":
        return int.from_bytes(file.read(size), byteorder="little", signed=False)
    elif data_type == "unsigned long":
        return int.from_bytes(file.read(size), byteorder="little", signed=False)
    elif data_type == "int":
        return int.from_bytes(file.read(size), byteorder="little", signed=False)
    elif data_type == "float":
        return struct.unpack("<f", file.read(size))[0]
    elif data_type == "":
        return "Image data"
    else:
        return None


def get_char(byte_value):
    """
    Convert a sequence of bytes to a string of characters.

    Args:
        byte_value (bytes): The sequence of bytes to convert.

    Returns:
        str: The string of characters obtained from the bytes.
    """
    accumulated_characters = ""
    for byte in byte_value:
        character = chr(byte)
        accumulated_characters += character
    return accumulated_characters


def get_module_data(module, file):
    """
    Read and extract data from a binary file based on the module's elements.

    Args:
        module (Module): The Module instance containing element information.
        file (file object): The binary file object to read from.

    Returns:
        dict: A dictionary containing extracted data from the file.
    """
    data_dictionary = {}
    for element in module.elements:
        value = read_element(file, element.datatype, element.length)
        if element.datatype == "char":
            char_value = get_char(value)
            data_dictionary[element.name] = char_value
        else:
            data_dictionary[element.name] = value
    return data_dictionary


def print_data_dictionary(data_dictionary, module_name, module_number=""):
    """
    Print the contents of a data dictionary in a formatted manner.

    Args:
        data_dictionary (dict): The dictionary containing data to be printed.
        module_name (str): The name of the module associated with the data.
        module_number (str, optional): The module number, if applicable.

    Returns:
        None
    """
    if module_number:
        module_number_str = module_number
    else:
        module_number_str = ""

    print(f"------{module_name} {module_number_str}------")
    for key, value in data_dictionary.items():
        print(f"{key} : {value}")


def system_setup_data(file):
    """
    Extract system setup information from a binary file.

    Args:
        file (str): The path to the binary file.

    Returns:
        dict: A dictionary containing extracted system setup information.
    """
    with open(file, "rb") as file:
        file.seek(258)
        data = file.read(114)

        # Decode the binary data as UTF-8 and split into lines
        decoded_data = data.decode("utf-8")
        lines = decoded_data.split("\r\n")

        # Create a dictionary to store extracted information
        extracted_info = {}

        # Process each line
        for line in lines:
            if ":" in line:
                label, value = line.split(":", 1)
                extracted_info[label.strip()] = value.strip()
    return extracted_info


def process_metadata(file_path):
    """
    Process metadata from a binary file and print relevant information.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        None
    """
    with open(file_path, "rb") as file:
        module_data_flio_header = get_module_data(flioheader, file)
        print_data_dictionary(module_data_flio_header, flioheader.name)

        extracted_info = file_information(file_path)

        print("------File Info ------")
        for label, value in extracted_info.items():
            print(f"{label}: {value}")

        extracted_system_setup_data = system_setup_data(file_path)
        print("------System Setup Data ------")
        for label, value in extracted_system_setup_data.items():
            print(f"{label}: {value}")

        meas_desc_block_offset_1 = module_data_flio_header.get("meas_desc_block_offset")
        file.seek(int(meas_desc_block_offset_1))
        module_data_flio_measurement = get_module_data(fliomeasurement, file)
        print_data_dictionary(module_data_flio_measurement, fliomeasurement.name, "0")

        meas_desc_block_offset_2 = (
            module_data_flio_header.get("meas_desc_block_offset")
            + (
                module_data_flio_header.get("data_block_offset")
                - module_data_flio_header.get("meas_desc_block_offset")
            )
            / 2
        )
        file.seek(int(meas_desc_block_offset_2))
        module_data_flio_measurement = get_module_data(fliomeasurement, file)
        print_data_dictionary(module_data_flio_measurement, fliomeasurement.name, "1")

        data_block_offset = module_data_flio_header.get("data_block_offset")
        file.seek(int(data_block_offset))
        module_data_datablock = get_module_data(datablock, file)
        print_data_dictionary(module_data_datablock, datablock.name, "0")

        # 8*256^3 + 22 + 770
        data_block_length = (
            module_data_flio_header.get("data_block_length") + data_block_offset
        )

        file.seek(int(data_block_length))
        module_data_data_datablock = get_module_data(datablock, file)
        print_data_dictionary(module_data_data_datablock, datablock.name, "1")


def image_summary_view(file_path):
    """
    Generate and display summary views of images from binary data blocks.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        None
    """
    with open(file_path, "rb") as file:
        module_data_flio_header = get_module_data(flioheader, file)
        img_size = 256
        array = np.fromfile(file_path, dtype="<H")
        offset = int((module_data_flio_header.get("data_block_offset") + 22) / 2)
        pixel_array = array[offset : offset + img_size**2 * 1024].reshape(
            256, 256, 1024
        )

        avg_pixel_array = np.average(pixel_array, axis=2)
        plt.suptitle(
            "from Datablock 0 - image shape: 256*256*1024, average of 1024 slices:"
        )
        plt.imshow(avg_pixel_array)
        plt.show()

        offset2 = int(
            (
                module_data_flio_header.get("data_block_length")
                + module_data_flio_header.get("data_block_offset")
                + 22
            )
            / 2
        )
        pixel_array = array[offset2 : offset2 + img_size**2 * 1024].reshape(
            256, 256, 1024
        )

        avg_pixel_array = np.average(pixel_array, axis=2)
        plt.suptitle(
            "from Datablock 1 - image shape: 256*256*1024, average of 1024 slices:"
        )
        plt.imshow(avg_pixel_array)
        plt.show()


# block number is 0 or 1 and slice number is between 0 and 1023
def image_slice_view(file_path, block_number, slice_number):
    """
    Generate and display a specific slice of an image from a binary data block.

    Args:
        file_path (str): The path to the binary file.
        block_number (int): The data block number (0 or 1).
        slice_number (int): The slice number to display.

    Returns:
        None
    """
    with open(file_path, "rb") as file:
        module_data_flio_header = get_module_data(flioheader, file)

    if block_number == 0:
        img_size = 256
        array = np.fromfile(file_path, dtype="<H")
        offset = int((module_data_flio_header.get("data_block_offset") + 22) / 2)
        pixel_array = array[offset : offset + img_size**2 * 1024].reshape(
            256, 256, 1024
        )

        plt.suptitle(f"from Datablock{block_number}, slicenumber: {slice_number} ")
        plt.imshow(pixel_array[:, :, slice_number])
        plt.show()

    elif block_number == 1:
        img_size = 256
        array = np.fromfile(file_path, dtype="<H")
        offset2 = int(
            (
                module_data_flio_header.get("data_block_length")
                + module_data_flio_header.get("data_block_offset")
                + 22
            )
            / 2
        )
        pixel_array = array[offset2 : offset2 + img_size**2 * 1024].reshape(
            256, 256, 1024
        )

        plt.suptitle(f"from Datablock{block_number}, slicenumber: {slice_number} ")

        plt.imshow(pixel_array[:, :, slice_number])
        plt.show
