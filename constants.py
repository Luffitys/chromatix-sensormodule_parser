# /usr/bin/env python3


# byte length of data types
# INT and UINT have the same size, but differ in functionality
class Types:
    INT8 = UINT8 = 1
    INT16 = UINT16 = 2
    INT32 = UINT32 = 4
    INT64 = UINT64 = 8


# variables ending with _LEN define a length
# lengths are in bytes
class Chromatix:
    # Constants as defined in Chromatix Data Access Design document
    TAG = "QTI Chromatix Header"
    TAG_LEN = 28  # INT32
    TOOL_LEN = 48  # INT32
    BINARY_TAG_LEN = 64  # INT32
    MAX_SECTIONS = 4  # INT32
    SECTION_SIZE = 12  # INT32


# Added, not from Chromatix
class Sensormodule:
    EOF_OFFSET_LEN = Types.INT32  # INT32
    MAJOR_LEN = Types.INT16  # INT16
    MINOR_LEN = Types.INT16  # INT16
    PATCH_LEN = Types.INT32  # INT32
    COMPRESSED_LEN = Types.INT32  # INT32
    CRC32_LEN = Types.INT32

    HEADER_LEN = (
        Chromatix.TAG_LEN
        + Types.INT32  # EOF_OFFSET_LEN
        + MAJOR_LEN  # MAJOR
        + MINOR_LEN  # MINOR
        + PATCH_LEN  # PATCH
        + Chromatix.TOOL_LEN
        + Chromatix.BINARY_TAG_LEN
        + Types.INT64  # unmapped
        + Types.INT32  # unmapped
        + Types.INT32  # unmapped
    )  # UINT32

    hsLength = HEADER_LEN + Chromatix.MAX_SECTIONS * Chromatix.SECTION_SIZE + 100

    # length of text like:
    # sensorDriverData cameraModuleData flashDriverData actuatorDriver OISDriver EEPROMDriverData PDConfigData
    # if text length < 16 then rest is padded with 0's to match length of 16
    headerText = 4 * Types.INT32
    # header text has a spacing of 40 bytes in between them filled with data
    # 4 bytes in front of the text has current module index
    headerTextSpacing = 10 * Types.INT32
