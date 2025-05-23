# /usr/bin/env python3

import os
from colorama import init, Fore, Style
import parse_header
import helpers


def parse(sensormodule):
    (data, sections) = parse_header.read_header_info(sensormodule)

    if helpers.compare_crc32(data["crc32"], data["crc32_calculated"]):
        crc32_str = Fore.GREEN + "CRC32 match!" + Style.RESET_ALL
    else:
        crc32_str = Fore.RED + "CRC32 mismatch!" + Style.RESET_ALL

    print(
        f"Tag: {data["tag"]}\n"
        f"Tool: {data["tool"]}\n"
        f"Binary: {data["binary"]}\n"
        f"Binary CRC32: {data["crc32"]}\n"
        f"Calculated CRC32: {data["crc32_calculated"]}\n"
        f"{crc32_str}\n"
        f"EOF Offset: {data["eof_offset"]}\n"
        f"Revision Major: {data["revision_major"]}\n"
        f"Revision Minor: {data["revision_minor"]}\n"
        f"Revision Patch: {data["revision_patch"]}\n"
    )

    # Read sections are in order 5-1, we want it in 1-5
    sections.reverse()
    for section in sections:
        print(
            f"Section Info: {section["info"]}\n"
            f"Section Offset: {section["offset"]}\n"
            f"Section Length: {section["length"]}\n"
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
    init()
    parse_start()
