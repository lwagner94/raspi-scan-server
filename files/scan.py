#!/usr/bin/env python3

import sys
import uuid
from datetime import datetime
from pathlib import Path
from sh import touch, scanimage, convert, tiff2pdf, chown


def get_scan_dir():
    d = Path("/scan")
    return d

def get_pdf_path():
    filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".pdf"
    return get_scan_dir() / filename

def get_temp_file_path():
    return Path("/tmp") / (str(uuid.uuid1()) + ".tiff")


def scan_image(dpi):
    path = get_temp_file_path()
    scanimage("--format", "tiff",
              "--mode", "Color",
              "--resolution", str(dpi),
              _tty_out=False,
              _out=str(path))

    return path

def convert2pdf(image, pdf, grayscale, quality):
    if grayscale:
        convert(str(image),
                "-colorspace", "Gray",
                "-compress", "jpeg", "-quality", str(quality),
                str(pdf))
    else:
        tiff2pdf(str(image),
                 "-j", "-q", str(quality),
                 "-o", str(pdf))

def scan_and_convert(dpi, grayscale, quality):
    image = None
    try:
        print("Scanning image ................ ", end="", flush=True)
        image = scan_image(dpi)
        print("OK")
        print("Converting image ............... ", end="", flush=True)
        pdf_path = get_pdf_path()
        convert2pdf(image, pdf_path, grayscale, quality)
        print("OK")
        print("Setting permissions ............ ", end="", flush=True)
        chown("scan:scan", str(pdf_path))

        print("OK")
    finally:
        print("Removing temporary file......... OK")
        if image:
            image.unlink()

def file_action():
    pass

def scan_action():
    scan_and_convert(300, True, 90)

def copy_action():
    scan_and_convert(300, False, 95)

def email_action():
    scan_and_convert(600, False, 100)


def main():
    if len(sys.argv) != 2:
        print(f"Error: Insufficient number of arguments: {sys.argv}")

    action = sys.argv[1]

    if action == "file":
        file_action()
    if action == "scan":
        scan_action()
    if action == "copy":
        copy_action()
    if action == "email":
        email_action()
    

if __name__ == "__main__":
    main()