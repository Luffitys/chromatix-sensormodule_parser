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
    read_utf8 = lambda length: helpers.byte_to_utf8(sensormodule.read(length))
    read_int = lambda length: helpers.byte_to_int(sensormodule.read(length))

    data = {}

    data["tag"] = read_utf8(constants.Chromatix.TAG_LEN)

    data["eof_offset"] = read_int(constants.Sensormodule.EOF_OFFSET_LEN)
    eof_offset = data["eof_offset"]

    data["crc32"] = read_crc32(sensormodule, eof_offset)
    data["crc32_calculated"] = calculate_crc32(sensormodule, eof_offset)

    data["revision_major"] = read_int(constants.Sensormodule.MAJOR_LEN)
    data["revision_minor"] = read_int(constants.Sensormodule.MINOR_LEN)
    data["revision_patch"] = read_int(constants.Sensormodule.PATCH_LEN)

    data["tool"] = read_utf8(constants.Chromatix.TOOL_LEN)
    data["binary"] = read_utf8(constants.Chromatix.BINARY_TAG_LEN)

    if data["revision_major"] != 5:
        print("Only Chromatix Major Version 5 is supported.")
        print(
            f"Chromatix Major Version {data['revision_major']} is not supported! Aborting.."
        )
        sys.exit()

    sections = read_header_data(sensormodule, data["eof_offset"])
    return data, sections


def read_header_data(sensormodule, eof_offset):
    index = helpers.byte_to_int(sensormodule.read(constants.Types.UINT64))
    info = {
        5: "Offset to end of header",
        4: "First Block",
        3: "Second Block",
        2: "Third (DEFAULT) Block",
        1: "Fourth Block (until EOF)",
    }
    offset = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    sections = [{"info": None, "offset": None, "length": None} for _ in range(index)]
    sections[index - 1]["info"] = info[index]
    sections[index - 1]["offset"] = offset
    sections[index - 1]["length"] = eof_offset

    while index > 1:
        index = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
        if index == 4:
            sensormodule.seek(
                sensormodule.tell() + constants.Types.UINT32
            )  # index 4 has 4 reserved bytes, skip those
        offset = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
        length = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
        # Only fill info, if binary structure has exactly 5 sections
        if len(sections) == 5:
            sections[index - 1]["info"] = info[index]
        sections[index - 1]["offset"] = offset
        sections[index - 1]["length"] = length
    return sections
