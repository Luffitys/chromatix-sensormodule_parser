# /usr/bin/env python3


# length of data types
# INT and UINT have the same size, but differ in functionality
class Types:
    INT8 = UINT8 = 1
    INT16 = UINT16 = 2
    INT32 = UINT32 = 4
    INT64 = UINT64 = 8


# variables ending with _LEN define a length
# other variables are generally hardcoded Chromatix default values
class Chromatix:
    # Constants as defined in Chromatix Data Access Design document
    TAG = "QTI Chromatix Header"
    TAG_LEN = 28  # UINT32
    TOOL_LEN = 48  # UINT32
    BINARY_TAG_LEN = 64  # UINT32
    MAJOR = 5  # UINT16
    MINOR = 0  # UINT16
    PATCH = 0  # UINT32
    MODE_FLAGS_MAJOR = 5  # UINT16
    MODE_FLAGS_MINOR = 0  # UINT16
    MODE_FLAGS_PATCH = 0  # UINT32
    DATA_TABLE_MAJOR = 4  # UINT16
    DATA_TABLE_MINOR = 0  # UINT16
    DATA_TABLE_PATCH = 0  # UINT32
    FLAGS_MAJOR = 3  # UINT16
    FLAGS_MINOR = 0  # UINT16
    FLAGS_PATCH = 0  # UINT32
    LINK_MAJOR = 2  # UINT16
    LINK_MINOR = 0  # UINT16
    LINK_PATCH = 0  # UINT32
    MODE_TREE_MAJOR = 1  # UINT16
    MODE_TREE_MINOR = 0  # UINT16
    MODE_TREE_PATCH = 2  # UINT32
    ALIGNED_START_MAJOR = 1  # UINT16
    ALIGNED_START_MINOR = 1  # UINT16
    ALIGNED_START_PATCH = 0  # UINT32
    ALIGNED_END_MAJOR = 3  # UINT16
    ALIGNED_END_MINOR = 0  # UINT16
    ALIGNED_END_PATCH = 1  # UINT32
    MIN_SECTIONS = 2  # UINT32
    MAX_SECTIONS = 4  # UINT32
    SECTION_SIZE = 12  # UINT32
    SYMBOL_SECTION = 0  # UINT32
    DATA_SECTION = 1  # UINT32
    MODE_SECTION = 2  # UINT32
    DATA_TABLE_SECTION = 3  # UINT32
    SIZE_OFFSET = TAG_LEN  # Offset to write the file size # UINT32
    MODE_NAME_LEN = 32  # UINT32
    NOT_LINKED_ID = 0xFFFFFFFF  # UINT32
    FLAGS_PACKED = 0x01  # UINT64
    FLAGS_COMPRESSED = 0x02  # UINT64
    FLAGS_CRC32 = 0x04  # UINT64
    MODE_FLAGS_PRESERVE = 0x01  # UINT32


# Added, not from Chromatix
class Sensormodule:
    EOF_OFFSET_LEN = 4  # UINT32
    MAJOR_LEN = 2  # UINT16
    MINOR_LEN = 2  # UINT16
    PATCH_LEN = 4  # UINT32
    COMPRESSED_LEN = 4  # UINT32

    HEADER_LEN = (
        Chromatix.TAG_LEN
        + Types.UINT32  # EOF_OFFSET_LEN
        + Types.UINT16  # MAJOR
        + Types.UINT16  # MINOR
        + Types.UINT32  # PATCH
        + Chromatix.TOOL_LEN
        + Chromatix.BINARY_TAG_LEN
        + Types.UINT64  # unmapped
        + Types.UINT32  # unmapped
        + Types.UINT32  # unmapped
    )  # UINT32

    hsLength = HEADER_LEN + Chromatix.MAX_SECTIONS * Chromatix.SECTION_SIZE + 100


class Decompressor:
    TAG = 0x43544251  # UINT32 # String: QBTC
    TAG_POS = 0  # UINT32
    TAG_LEN = 4  # UINT32
    NUM_BITS_POS = TAG_POS + TAG_LEN  # UINT32
    NUM_BITS_LEN = 4  # UINT32
    FREQUENCY_POS = NUM_BITS_POS + NUM_BITS_LEN  # UINT32
    FREQUENCY_SIZE = 4  # UINT32
    FREQUENCY_COUNT = 256  # UINT32
    FREQUENCY_LEN = FREQUENCY_COUNT * FREQUENCY_SIZE  # UINT32
    DATA_POS = FREQUENCY_POS + FREQUENCY_LEN  # UINT32
