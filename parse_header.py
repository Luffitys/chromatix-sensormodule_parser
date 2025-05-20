# /usr/bin/env python3

import sys
import constants
import helpers


def read_crc32(sensormodule, eof_offset):
    crc32 = helpers.byte_to_hex_sequence(
        helpers.read_cursor(
            sensormodule, constants.Sensormodule.CRC32_LEN, initial_pos=eof_offset
        )
    )
    return crc32


def calculate_crc32(sensormodule, eof_offset):
    crc32 = helpers.calculate_crc32(
        helpers.read_cursor(sensormodule, eof_offset, initial_pos=0)
    )
    crc32_formatted = helpers.hex_switch_endian(helpers.remove_hex_prefix(crc32))
    return crc32_formatted


def read_header_info(sensormodule):
    tag = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.TAG_LEN))
    eof_offset = helpers.byte_to_int(
        sensormodule.read(constants.Sensormodule.EOF_OFFSET_LEN)
    )

    crc32 = read_crc32(sensormodule, eof_offset)
    calculated_crc32 = calculate_crc32(sensormodule, eof_offset)

    major = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.MAJOR_LEN))
    minor = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.MINOR_LEN))
    patch = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.PATCH_LEN))
    tool = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.TOOL_LEN))
    binary = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.BINARY_TAG_LEN))

    if major != 5:
        print("Only Chromatix Major Version 5 is supported.")
        print(f"Chromatix Major Version {major} is not supported! Aborting..")
        sys.exit()
    return tag, eof_offset, crc32, calculated_crc32, major, minor, patch, tool, binary


def read_header_data(sensormodule):
    index_of_curr_section1 = helpers.byte_to_int(
        sensormodule.read(constants.Types.UINT64)
    )
    header_end_offset = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))

    # theory
    index_of_curr_section2 = helpers.byte_to_int(
        sensormodule.read(constants.Types.UINT32)
    )
    reserved1_bytes = helpers.byte_length(sensormodule.read(constants.Types.UINT32))
    offset_to_module1 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    length_of_module1 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))

    index_of_curr_section3 = helpers.byte_to_int(
        sensormodule.read(constants.Types.UINT32)
    )
    offset_to_module2 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    length_of_module2 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))

    index_of_curr_section4 = helpers.byte_to_int(
        sensormodule.read(constants.Types.UINT32)
    )
    offset_to_module3 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    length_of_module3 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))

    index_of_curr_section5 = helpers.byte_to_int(
        sensormodule.read(constants.Types.UINT32)
    )
    offset_to_module4 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    length_of_module4 = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))

    return (
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
    )
