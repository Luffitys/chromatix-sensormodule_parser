# /usr/bin/env python3

import os
import parse_header


def parse(sensormodule):
    (
        tag,
        eof_offset,
        major,
        minor,
        patch,
        tool,
        binary,
    ) = parse_header.read_header_info(sensormodule)
    print(
        f"Tag: {tag}\n"
        f"EofOffset: {eof_offset}\n"
        f"Major: {major}\n"
        f"Minor: {minor}\n"
        f"Patch: {patch}\n"
        f"Tool: {tool}\n"
        f"Binary: {binary}"
    )
    (unmapped1_value, unmapped2_value, unmapped3_value, reserved_length) = (
        parse_header.read_header_data(sensormodule)
    )
    print(
        f"Unmapped_value: {unmapped1_value}\n"
        f"Unmapped_value: {unmapped2_value}\n"
        f"Unmapped_value: {unmapped3_value}\n"
        f"Reserved_length: {reserved_length}"
    )


def parse_start():
    # filename = input('\nEnter the full file name of your sensormodule .bin\nExample: com.qti.sensormodule.sunny_ov64b40_tele.bin\n------\n: ')
    # hardcode it for testing purposes
    filename = "com.qti.sensormodule.sunny_ov64b40_tele.bin"

    if not os.path.exists(filename):
        print(f"The selected file {filename} doesn't exist. Aborting..")
        return

    with open(filename, "rb") as sensormodule:
        parse(sensormodule)


if __name__ == "__main__":
    parse_start()
