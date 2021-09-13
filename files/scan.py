#!/usr/bin/env python3

import sys
import uuid
import time
from datetime import datetime
from pathlib import Path
from sh import touch, scanimage, convert, tiff2pdf, chown, cp, pdfunite
import os
from multiprocessing import Process


# def detachify(func):
#     """Decorate a function so that its calls are async in a detached process.

#     Usage
#     -----

#     .. code::
#             import time

#             @detachify
#             def f(message):
#                 time.sleep(5)
#                 print(message)

#             f('Async and detached!!!')

#     """
#     # create a process fork and run the function
#     def forkify(*args, **kwargs):
#         if os.fork() != 0:
#             return
#         func(*args, **kwargs)

#     # wrapper to run the forkified function
#     def wrapper(*args, **kwargs):
#         proc = Process(target=lambda: forkify(*args, **kwargs))
#         proc.start()
#         proc.join()
#         return

#     return wrapper


def get_scan_dir():
    d = Path("/scan")
    return d

def get_pdf_path():
    filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".pdf"
    return get_scan_dir() / filename

def get_tiff_path():
    filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".tiff"
    return get_scan_dir() / filename

def get_temp_file_path():
    return Path("/tmp") / (str(uuid.uuid1()) + ".tiff")


def scan_image(dpi):
    path = get_temp_file_path()
    scanimage("--format", "tiff",
              "--mode", "Color",
              "--resolution", str(dpi),
              "-x", "210",
              "-y", "297",
              _tty_out=False,
              _out=str(path))

    return path

def convert2pdf(image, pdf, quality):
    convert(str(image),
            "-compress", "jpeg", "-quality", str(quality),
            str(pdf))


def scan_and_convert(dpi, quality):
    image = None
    try:
        print("Scanning image ................ ", end="", flush=True)
        image = scan_image(dpi)
        print("OK")
        print("Converting image ............... ", end="", flush=True)
        pdf_path = get_pdf_path()
        a = datetime.now()
        convert2pdf(image, pdf_path, quality)
        b = datetime.now()
        print("OK")
        print("Took: ", b-a)
        print("Setting permissions ............ ", end="", flush=True)
        chown("scan:scan", str(pdf_path))

        print("OK")
    finally:
        print("Removing temporary file......... OK")
        if image:
            image.unlink()

def scan_without_conversion(dpi):
    image = None
    try:
        print("Scanning image ................ ", end="", flush=True)
        image = scan_image(dpi)
        print("OK")
        print("Converting image ............... ", end="", flush=True)
        pdf_path = get_tiff_path()
        # Copy
        cp(image, pdf_path)
        print("OK")
        print("Setting permissions ............ ", end="", flush=True)
        chown("scan:scan", str(pdf_path))

        print("OK")
    finally:
        print("Removing temporary file......... OK")
        if image:
            image.unlink()

def merge():
    print("Merging last two PDFs ............ ", end="", flush=True)
    scan_dir = get_scan_dir()
    all_pdfs = sorted(scan_dir.glob("*.pdf"))

    if len(all_pdfs) >= 2:
        current_scan = all_pdfs[-1]
        last_scan = all_pdfs[-2]
        pdfunite(last_scan, current_scan, get_pdf_path())
        current_scan.unlink()
        last_scan.unlink()

    print("OK")

    
#@detachify
def test():
    time.sleep(10)
    print("Hello", flush=True)

def file_action():
    scan_and_convert(150, 60)

def extra_action():
    scan_and_convert(150, 60)
    merge()

def scan_action():
    scan_without_conversion(600)

def copy_action():
    pass

def email_action():
    print("instant", flush=True)
    test()
    pass
    

def main():
    if len(sys.argv) != 2:
        print(f"Error: Insufficient number of arguments: {sys.argv}")

    action = sys.argv[1]

    if action == "file":
        file_action()

    if action == "extra":
        extra_action()
    if action == "scan":
        scan_action()
    if action == "copy":
        copy_action()
    if action == "email":
        email_action()
    

if __name__ == "__main__":
    main()
    