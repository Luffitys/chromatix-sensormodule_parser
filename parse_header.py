# /usr/bin/env python3

import sys
import constants
import helpers


def read_header_info(sensormodule):
    sensormodule.seek(0)
    tag = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.TAG_LEN))
    eof_offset = helpers.byte_to_int(
        sensormodule.read(constants.Sensormodule.EOF_OFFSET_LEN)
    )
    major = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.MAJOR_LEN))
    minor = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.MINOR_LEN))
    patch = helpers.byte_to_int(sensormodule.read(constants.Sensormodule.PATCH_LEN))
    tool = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.TOOL_LEN))
    binary = helpers.byte_to_utf8(sensormodule.read(constants.Chromatix.BINARY_TAG_LEN))

    if major != 5:
        print("Only Chromatix Major Version 5 is supported.")
        print(f"Chromatix Major Version {major} is not supported! Aborting..")
        sys.exit()
    return tag, eof_offset, major, minor, patch, tool, binary


def read_header_data(sensormodule):
    unmapped1_value = helpers.byte_to_int(sensormodule.read(constants.Types.UINT64))
    unmapped2_value = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    unmapped3_value = helpers.byte_to_int(sensormodule.read(constants.Types.UINT32))
    reserved_length = helpers.byte_length(sensormodule.read(constants.Types.UINT32))
    return unmapped1_value, unmapped2_value, unmapped3_value, reserved_length
