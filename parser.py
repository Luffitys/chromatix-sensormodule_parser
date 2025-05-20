# /usr/bin/env python3

import os
import parse_header


def parse(sensormodule):
    (
        tag,
        eof_offset,
        crc32,
        calculated_crc32,
        major,
        minor,
        patch,
        tool,
        binary,
    ) = parse_header.read_header_info(sensormodule)
    if crc32 == calculated_crc32:
        crc32_str = "Calculated CRC32 matches the Binary CRC32"
    else:
        crc32_str = "Calculated CRC32 does not match the Binary CRC32. The file has probably been modified!"
    print(
        f"Tag: {tag}\n"
        f"EOF Offset: {eof_offset}\n"
        f"Binary CRC32: {crc32}\n"
        f"Calculated CRC32: {calculated_crc32}\n"
        f"{crc32_str}\n"
        f"Major: {major}\n"
        f"Minor: {minor}\n"
        f"Patch: {patch}\n"
        f"Tool: {tool}\n"
        f"Binary: {binary}\n"
    )
    (
        index_of_curr_section1,
        header_end_offset,
        index_of_curr_section2,
        reserved1_bytes,
        offset_to_module1,
        length_of_module1,
        index_of_curr_section3,
        offset_to_module2,
        length_of_module2,
        index_of_curr_section4,
        offset_to_module3,
        length_of_module3,
        index_of_curr_section5,
        offset_to_module4,
        length_of_module4,
    ) = parse_header.read_header_data(sensormodule)
    print("TODO: read first section index int, then loop until index = 1\n")
    print(
        f"index of current section: {index_of_curr_section1}\n"
        f"offset of current module: {header_end_offset} # end of header\n\n"
        f"index of current section: {index_of_curr_section2}\n"
        f"bytes_reserved: {reserved1_bytes}\n"
        f"offset to module: {offset_to_module1} # first block (list of all offsets)\n"
        f"byte_length of module: {length_of_module1}\n\n"
        f"index of current section: {index_of_curr_section3}\n"
        f"offset of current module: {offset_to_module2} # second block\n"
        f"byte_length of module: {length_of_module2}\n\n"
        f"index of current section: {index_of_curr_section4}\n"
        f"offset of current module: {offset_to_module3} # DEFAULT block\n"
        f"byte_length of module: {length_of_module3}\n\n"
        f"index of current section: {index_of_curr_section5}\n"
        f"offset of current module: {offset_to_module4} # EOF\n"
        f"byte_length of module: {length_of_module4}\n\n"
    )


def parse_start():
    # filename = input('\nEnter the full file name of your sensormodule .bin\nExample: com.qti.sensormodule.sunny_ov64b40_tele.bin\n------\n: ')
    # hardcode it for testing purposes
    filename = "com.qti.sensormodule.sunny_ov64b40_tele.bin"

    if not os.path.exists(filename):
        print(f"The selected file {filename} doesn't exist. Aborting..")
        return

    with open(filename, "rb") as sensormodule:
        parse(sensormodule)


if __name__ == "__main__":
    parse_start()
