#!/usr/bin/env python3
"""
A3 PDF to A4 PDF splitter
Splits A3 PDF pages horizontally into two A4 pages
"""
import PyPDF2
import sys
import os
import re
from pathlib import Path

def split_a3_to_a4(input_file):
    """
    Split A3 PDF pages into A4 pages

    Args:
        input_file: Path to the input PDF file

    Returns:
        Output filename if successful, None if error
    """
    try:
        # Generate output filename
        input_path = Path(input_file)
        output_filename = input_path.stem + '_A4.pdf'
        output_path = input_path.parent / output_filename

        # Open PDF
        with open(input_file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            # Process each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]

                # Get page dimensions
                mediabox = page.mediabox
                x0, y0 = float(mediabox.lower_left[0]), float(mediabox.lower_left[1])
                x1, y1 = float(mediabox.upper_right[0]), float(mediabox.upper_right[1])

                # Calculate page width and height
                width = x1 - x0
                height = y1 - y0

                # Determine if page is landscape (A3 orientation)
                if width > height:
                    # Split horizontally (left and right)
                    mid_x = x0 + width / 2

                    # Left page (first half)
                    left_page = pdf_reader.pages[page_num]
                    left_page.cropbox.lower_left = (x0, y0)
                    left_page.cropbox.upper_right = (mid_x, y1)

                    # Right page (second half)
                    right_page = pdf_reader.pages[page_num]
                    right_page.cropbox.lower_left = (mid_x, y0)
                    right_page.cropbox.upper_right = (x1, y1)

                    # Add pages in order (left first, then right)
                    pdf_writer.add_page(left_page)
                    pdf_writer.add_page(right_page)
                else:
                    # Split vertically (top and bottom) for portrait orientation
                    mid_y = y0 + height / 2

                    # Top page (first half)
                    top_page = pdf_reader.pages[page_num]
                    top_page.cropbox.lower_left = (x0, mid_y)
                    top_page.cropbox.upper_right = (x1, y1)

                    # Bottom page (second half)
                    bottom_page = pdf_reader.pages[page_num]
                    bottom_page.cropbox.lower_left = (x0, y0)
                    bottom_page.cropbox.upper_right = (x1, mid_y)

                    # Add pages in order (top first, then bottom)
                    pdf_writer.add_page(top_page)
                    pdf_writer.add_page(bottom_page)

            # Write output file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"Successfully split PDF: {output_path}")
            return str(output_path)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python pdf_a3_to_a4.py <input_pdf_file>")
        print("Example: python pdf_a3_to_a4.py document.pdf")
        sys.exit(1)

    input_file = sys.argv[1]

    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    # Check if it's a PDF file
    if not input_file.lower().endswith('.pdf'):
        print("Error: Input file must be a PDF file.")
        sys.exit(1)

    # Process the PDF
    result = split_a3_to_a4(input_file)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()