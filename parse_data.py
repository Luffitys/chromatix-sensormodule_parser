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
        {"resolution_x": None, "resolution_y": None, "mode": None, "offset": None}
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
    for section in sections[:]:
        if section["resolution_y"] < 100:  # Drop useless resolutions
            is_ignore[iter]["ignore"] = True
            iter += 1
    return sections, is_ignore


def get_resolution_data(sensormodule, resolutions):
    data = {}
    return data
