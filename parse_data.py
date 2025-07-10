# /usr/bin/env python3

import helpers
import constants


def get_resolutions(sensormodule):
    read_int = lambda length: helpers.byte_to_int(sensormodule.read(length))
    sensormodule.seek(0)
    data = sensormodule.read()

    resolution_10bit_bytes = helpers.utf8_to_byte("0A0000000100000000000000")
    resolution_12bit_bytes = helpers.utf8_to_byte("0C0000000100000000000000")
    shdr_bytes = "0A0000000500000000000000"
    resolution_len = len(resolution_10bit_bytes)
    hits = data.count(resolution_10bit_bytes) + data.count(resolution_12bit_bytes)
    sections = [
        {
            "resolution_x": None,
            "resolution_y": None,
            "mode": None,
            "isInherited": "TBD",
            "sHDR": None,
            "offset": None,
            "hasPDAF": False,
            "slaveAddr": None,
        }
        for _ in range(hits)
    ]

    i = 0
    j = 0
    while i <= len(data) - resolution_len:
        if data[i : i + resolution_len] in (
            resolution_10bit_bytes,
            resolution_12bit_bytes,
        ):
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
        elif mode == 44:  # 0x2C
            mode = "12-bit RAW"
        section["mode"] = mode
        is_ignore[iter]["id"] = iter
        iter += 1

    iter = 0
    for section in sections:
        if section["resolution_y"] < 100:  # Drop useless resolutions below res_y=100px
            is_ignore[iter]["ignore"] = True
            iter += 1

    pdaf_offsets = [68, 144, 6104]
    for section in sections:
        sensormodule.seek(section["offset"])
        for offset in pdaf_offsets:
            sensormodule.seek(section["offset"] + offset)
            buffer = helpers.byte_to_hex_sequence(sensormodule.read(2))
            if buffer == "7004":
                section["hasPDAF"] = True

    reg_offsets = [
        56,
        72,
        132,
        148,
        172,
        176,
        188,
        208,
        216,
        248,
        352,
        456,
        524,
        820,
        1192,
    ]
    for section in sections:
        sensormodule.seek(section["offset"])
        for offset in reg_offsets:
            sensormodule.seek(section["offset"] + offset)
            buffer = helpers.byte_to_hex_sequence(sensormodule.read(2))
            if buffer in ("1201", "0832", "0403"):
                sensormodule.seek(sensormodule.tell() - 6)
                section["slaveAddr"] = helpers.byte_to_hex_sequence(
                    sensormodule.read(4)
                )

        sensormodule.seek(section["offset"])
        buffer = helpers.byte_to_hex_sequence(sensormodule.read(216))
        if shdr_bytes in buffer:
            section["sHDR"] = True

    return sections, is_ignore


def get_resolution_data(sensormodule, resolutions):
    data = {}
    return data
