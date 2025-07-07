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

    header_sections = read_header_sections(sensormodule, data["eof_offset"])
    module_sections, global_offset = read_module_sections(sensormodule)
    return data, header_sections, module_sections, global_offset


def read_header_sections(sensormodule, eof_offset):
    index = helpers.byte_to_int(sensormodule.read(constants.Types.INT64))
    info = {
        5: "Offset to end of header",
        4: "First Block",
        3: "Second Block",
        2: "Third (DEFAULT) Block",
        1: "Last Block (until EOF)",
    }
    offset = helpers.byte_to_int(sensormodule.read(constants.Types.INT32))
    sections = [{"info": None, "offset": None, "length": None} for _ in range(index)]
    sections[index - 1]["info"] = info[index]
    sections[index - 1]["offset"] = offset
    sections[index - 1]["length"] = eof_offset

    while index > 1:
        index = helpers.byte_to_int(sensormodule.read(constants.Types.INT32))
        # index 4 has 4 reserved bytes, skip those
        if index == 4:
            sensormodule.seek(sensormodule.tell() + constants.Types.INT32)
        offset = helpers.byte_to_int(sensormodule.read(constants.Types.INT32))
        length = helpers.byte_to_int(sensormodule.read(constants.Types.INT32))
        # Only fill info, if binary structure has exactly 5 sections
        if len(sections) == 5:
            sections[index - 1]["info"] = info[index]
        sections[index - 1]["offset"] = offset
        sections[index - 1]["length"] = length
    return sections


def read_module_sections(sensormodule):
    read_utf8 = lambda length: helpers.byte_to_utf8(sensormodule.read(length))
    read_int = lambda length: helpers.byte_to_int(sensormodule.read(length))

    data = helpers.read_cursor(
        sensormodule, 1023, initial_pos=0, end_pos=sensormodule.tell()
    )
    if "OISDriver".encode() in data:
        iterations = 7
    else:
        iterations = 6
    sections = [
        {"string": None, "offset": None, "length": None} for _ in range(iterations)
    ]

    index = 1
    while index < iterations:
        index = read_int(constants.Types.INT32)
        sections[index - 1]["string"] = read_utf8(16)
        sensormodule.seek(sensormodule.tell() + 28)
        sections[index - 1]["offset"] = read_int(constants.Types.INT32)
        sections[index - 1]["length"] = read_int(constants.Types.INT32)
        sensormodule.seek(
            sensormodule.tell() + constants.Types.INT32
        )  # skip index duplicate
    global_offset = sensormodule.tell()
    for entry in sections:
        entry[
            "offset"
        ] += global_offset  # Read offsets are don't include the entire length of the header + sections, so add that length
    return sections, global_offset
