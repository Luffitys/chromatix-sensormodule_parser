# /usr/bin/env python3

import zlib


def byte_to_int(byte_sequence):
    return int.from_bytes(byte_sequence, "little")


def byte_to_utf8(byte_sequence):
    return byte_sequence.decode("utf-8").strip("\x00")


def utf8_to_byte(string):
    return bytes.fromhex(string)


def byte_to_hex_sequence(byte_sequence):
    return byte_sequence.hex().upper()


def byte_length(byte_sequence):
    return len(byte_sequence)


def calculate_crc32(byte_sequence):
    return hex(zlib.crc32(byte_sequence)).upper()


def compare_crc32(crc32_1, crc32_2):
    return crc32_1 == crc32_2


def hex_switch_endian(hex_string):
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    reversed_hex = bytearray.fromhex(hex_string)
    reversed_hex.reverse()
    reversed_hex_string = "".join(format(x, "02x") for x in reversed_hex).upper()
    return reversed_hex_string


def read_cursor(buffer, length, initial_pos=None, end_pos=None):
    pos = buffer.tell()
    if initial_pos is not None:
        buffer.seek(initial_pos)
    byte_sequence = buffer.read(length)
    if end_pos is not None:
        buffer.seek(end_pos)
    else:
        buffer.seek(pos)
    return byte_sequence


def remove_hex_prefix(string):
    return string[2:]
