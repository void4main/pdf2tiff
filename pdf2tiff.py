#!/usr/bin/env python3

"""
pdf2tiff.py: Converts one page of a PDF into a compressed TIFF file.

Example: pdf2tiff -f file.pdf -p 10
"""

""" 
pip uninstall fitz
pip install --upgrade --force-reinstall pymupdf
pip install pillow
pip install frontend
"""

__author__ = "Frank Hoffmann"
__version__ = "0.1.5"

import os
from pathlib import Path
from argparse import ArgumentParser
import fitz  # Install PyMuPDF, do _not_ install fitz
from PIL import Image

"""
DPI = 600, size of render from PDF
THRESHOLD = 140, for grayscale / bw conversion
"""
DPI = 600
THRESHOLD = 140

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="PDF file", metavar="<FILE>", required=True)
    parser.add_argument("-p", "--page", dest="page",
                        help="Page number to convert", metavar="<PAGE>", type=int, required=True)
    args = parser.parse_args()

    pdf_file_path = getattr(args, 'filename')
    if not os.path.isfile(pdf_file_path):
        print("Error: File not found: " + pdf_file_path)
        exit(1)
    page_number = getattr(args, 'page')
    output_file_path = Path(pdf_file_path).stem + "-" + str(page_number) + ".tiff"

    # Build PNG first
    document = fitz.open(pdf_file_path)
    page = document.load_page(page_number - 1)
    pix = page.get_pixmap(dpi=DPI)

    # Covert to PIL
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)

    # Grayscale
    fn = lambda x: 255 if x > THRESHOLD else 0
    image_convert = image.convert('L').point(fn, mode='1')

    # Compress TIFF and save to file
    image_convert.save(output_file_path, 'TIFF', compression='group4')

    exit(0)