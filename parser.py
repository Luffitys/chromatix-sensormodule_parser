# /usr/bin/env python3

import os
from colorama import init
import parse_header, parse_data
import helpers


def parse(sensormodule):
    (data, header_sections, module_sections) = parse_header.read_header_info(
        sensormodule
    )

    if helpers.compare_crc32(data["crc32"], data["crc32_calculated"]):
        crc32_str = helpers.print_format_color("CRC32 match!", "green")
    else:
        crc32_str = helpers.print_format_color("CRC32 mismatch!", "red")

    print(helpers.print_format_color("::::::::::HEADER INFO::::::::::", "green"))

    print(
        f"Tag: {data["tag"]}\n"
        f"Tool: {data["tool"]}\n"
        f"Binary: {data["binary"]}\n"
        f"Binary CRC32: {data["crc32"]}\n"
        f"Calculated CRC32: {data["crc32_calculated"]}\n"
        f"{crc32_str}\n"
        f"EOF Offset: {data["eof_offset"]}\n"
        f"Revision: {data["revision_major"]}.{data["revision_minor"]}.{data["revision_patch"]}\n"
    )

    print()

    print(helpers.print_format_color("::::::::::SECTION INFO::::::::::", "green"))

    # Read sections are in order 5-1, we want it in 1-5
    header_sections.reverse()
    for section in header_sections:
        print(
            f"Section Info: {section["info"]}\n"
            f"Section Offset: {section["offset"]}\n"
            f"Section Length: {section["length"]}\n"
        )

    print(helpers.print_format_color("::::::::::MODULE INFO::::::::::", "green"))

    print()
    for section in module_sections:
        print(
            f"Module: {section["string"]}\n"
            f"Module Offset: {section["offset"]}\n"
            f"Module Length: {section["length"]}\n"
        )

    print()

    print(helpers.print_format_color("::::::::::RESOLUTION INFO::::::::::", "green"))

    resolutions = parse_data.get_resolutions(sensormodule)
    for resolution in resolutions:
        print(f"Resolution: {resolution["resolution_x"]}x{resolution["resolution_y"]}")
        print(f"Crop Resolution: {resolution["crop_x"]}x{resolution["crop_y"]}")
        print(f"Mode: {resolution["mode"]}")
        print(f"Offset: {resolution["offset"]}\n")


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
    init()
    parse_start()
