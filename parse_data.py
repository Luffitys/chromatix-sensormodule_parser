# /usr/bin/env python3

import helpers
import constants


def get_resolutions(sensormodule):
    read_int = lambda length: helpers.byte_to_int(sensormodule.read(length))
    sensormodule.seek(0)
    data = sensormodule.read()

    resolution_bytes = helpers.utf8_to_byte("0A0000000100000000000000")
    resolution_len = len(resolution_bytes)
    hits = data.count(resolution_bytes)
    sections = [
        {
            "resolution_x": None,
            "resolution_y": None,
            "mode": None,
            "isInherited": None,
            "sHDR": None,
            "offset": None,
            "hasPDAF": None,
            "shortSection": None,
            "slaveAddr_offset": None,
            "slaveAddr": None,
        }
        for _ in range(hits)
    ]

    i = 0
    j = 0
    while i <= len(data) - resolution_len:
        if data[i : i + resolution_len] == resolution_bytes:
            sections[j]["offset"] = i
            j += 1
            i += resolution_len  # Skip ahead by length of pattern (non-overlapping)
        else:
            i += 1

    is_ignore = [{"id": None, "ignore": False} for _ in range(len(sections))]
    iter = 0
    for section in sections:
        sensormodule.seek(section["offset"] - (2 * constants.Types.INT32 + 12))
        mode = read_int(constants.Types.INT32)
        section["crop_x"] = read_int(constants.Types.INT32)
        section["crop_y"] = read_int(constants.Types.INT32)
        section["resolution_x"] = read_int(constants.Types.INT32)
        section["resolution_y"] = read_int(constants.Types.INT32)

        if mode == 43:  # 0x2B
            mode = "10-bit RAW"
        section["mode"] = mode
        is_ignore[iter]["id"] = iter
        iter += 1

    iter = 0
    for section in sections:
        if section["resolution_y"] < 100:  # Drop useless resolutions
            is_ignore[iter]["ignore"] = True
            iter += 1

    for section in sections:
        sensormodule.seek(section["offset"])
        buffer1 = helpers.byte_to_hex_sequence(sensormodule.read(37))  # PDAF Validation
        if "0832" in buffer1:
            section["shortSection"] = False
        elif "0403" in buffer1:
            section["shortSection"] = False
        else:
            section["shortSection"] = True
        sensormodule.seek(sensormodule.tell() - 38)
        buffer2 = helpers.byte_to_hex_sequence(sensormodule.read(84))  # PDAF Validation
        if "0832" in buffer2:
            section["hasPDAF"] = False
        elif "0403" in buffer2:
            section["hasPDAF"] = False
        else:
            section["hasPDAF"] = True
        sensormodule.seek(sensormodule.tell() - 84)
        buffer3 = helpers.byte_to_hex_sequence(
            sensormodule.read(216)
        )  # PDAF Validation
        if "A0000000100000000000000" and "A0000000500000000000000" in buffer3:
            section["sHDR"] = True
        else:
            section["sHDR"] = False
    index = 0
    for section in sections:
        sensormodule.seek(section["offset"])
        if section["hasPDAF"] == True:
            if (
                index is not 1
                and section["shortSection"] == True
                and section["sHDR"] == False
            ):  # Index 1 has 4 Bytes more, even if shortSection is True
                section["slaveAddr_offset"] = (14 * constants.Types.INT32) + (
                    19 * constants.Types.INT32
                )
            elif section["sHDR"] == True:
                section["slaveAddr_offset"] = (14 * constants.Types.INT32) + (
                    40 * constants.Types.INT32
                )
            else:
                section["slaveAddr_offset"] = (14 * constants.Types.INT32) + (
                    23 * constants.Types.INT32
                )
        else:
            section["slaveAddr_offset"] = 14 * constants.Types.INT32
        sensormodule.seek(sensormodule.tell() + section["slaveAddr_offset"])
        section["slaveAddr"] = helpers.byte_to_hex_sequence(
            sensormodule.read(constants.Types.INT32)
        )
        index += 1

    for section in sections:
        if "0832" in section["slaveAddr"]:
            section["isInherited"] = False
        elif "0403" in section["slaveAddr"]:
            section["isInherited"] = False
        else:
            section["isInherited"] = True

    return sections, is_ignore


def get_resolution_data(sensormodule, resolutions):
    data = {}
    return data
