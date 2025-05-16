# /usr/bin/env python3


def byte_to_int(byte_sequence):
    return int.from_bytes(byte_sequence, "little")


def byte_to_utf8(byte_sequence):
    return byte_sequence.decode("utf-8").strip("\x00")


def byte_length(byte_sequence):
    return len(byte_sequence)
