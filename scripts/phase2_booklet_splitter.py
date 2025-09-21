#!/usr/bin/env python3
"""
Phase 2: Booklet PDF Splitter and Reorderer
A3製本PDFを分割して正しいA4ページ順に並び替えるツール
"""
import PyPDF2
import sys
import os
import re
from pathlib import Path
from optparse import OptionParser

def generate_booklet_mapping(total_pages):
    """
    Generate booklet page mapping using the discovered formula

    Args:
        total_pages: Total number of A4 pages in the final document (must be multiple of 4)

    Returns:
        List of tuples: (A3_sheet_number, [left_A4_page, right_A4_page])
    """
    # Ensure total_pages is multiple of 4
    if total_pages % 4 != 0:
        padded_pages = ((total_pages + 3) // 4) * 4
        print(f"Warning: {total_pages} pages padded to {padded_pages} pages")
        total_pages = padded_pages

    S = total_pages // 2  # Number of A3 sheets
    mapping = []

    for i in range(1, S + 1):  # A3 sheet numbers 1 to S
        j = i - 1  # 0-based index
        b = j % 2  # 0 for even positions, 1 for odd positions

        # Apply the formula from Codex analysis:
        # Left(i) = S + (2b - 1) * j + b
        # Right(i) = T + 1 - Left(i)
        left = S + (2 * b - 1) * j + b
        right = total_pages + 1 - left

        mapping.append((i, [left, right]))

    return mapping

def verify_mapping(total_pages=32):
    """Verify the mapping against known data"""

    # Known correct mapping for 32 pages
    known_mapping = [
        (1, [16, 17]), (2, [18, 15]), (3, [14, 19]), (4, [20, 13]),
        (5, [12, 21]), (6, [22, 11]), (7, [10, 23]), (8, [24, 9]),
        (9, [8, 25]), (10, [26, 7]), (11, [6, 27]), (12, [28, 5]),
        (13, [4, 29]), (14, [30, 3]), (15, [2, 31]), (16, [32, 1])
    ]

    generated = generate_booklet_mapping(total_pages)

    print("Verification of booklet mapping formula:")
    print("=" * 50)
    print("A3 | Generated | Known    | Match")
    print("-" * 50)

    matches = 0
    for gen, known in zip(generated, known_mapping):
        match = gen[1] == known[1]
        if match:
            matches += 1

        print(f"{gen[0]:2d} | {gen[1]}     | {known[1]}    | {'✓' if match else '✗'}")

    print(f"\nMatches: {matches}/{len(known_mapping)}")
    return matches == len(known_mapping)

def split_and_reorder_pdf(input_file, total_pages=None, rotate=False):
    """
    Split A3 PDF and reorder pages according to booklet pattern

    Args:
        input_file: Path to input A3 PDF
        total_pages: Total A4 pages (auto-detect if None)
        rotate: Whether to rotate pages 90 degrees

    Returns:
        Output filename if successful
    """
    try:
        with open(input_file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_a3_pages = len(pdf_reader.pages)

            # Auto-detect total pages if not specified
            if total_pages is None:
                total_pages = num_a3_pages * 2
                print(f"Auto-detected: {num_a3_pages} A3 pages = {total_pages} A4 pages")

            # Generate mapping
            mapping = generate_booklet_mapping(total_pages)

            # Create output filename
            input_path = Path(input_file)
            output_filename = input_path.stem + '_phase2_reordered.pdf'
            output_path = input_path.parent / output_filename

            # Split and collect all A4 pages first
            split_pages = {}  # {A4_page_number: PageObject}

            print(f"Splitting {num_a3_pages} A3 pages...")

            for a3_idx in range(num_a3_pages):
                if a3_idx >= len(mapping):
                    print(f"Warning: A3 page {a3_idx + 1} exceeds mapping, skipping")
                    break

                original_page = pdf_reader.pages[a3_idx]
                a3_sheet_num, [left_a4, right_a4] = mapping[a3_idx]

                # Get page dimensions
                mediabox = original_page.mediabox
                x0, y0 = float(mediabox.lower_left[0]), float(mediabox.lower_left[1])
                x1, y1 = float(mediabox.upper_right[0]), float(mediabox.upper_right[1])

                width = x1 - x0
                height = y1 - y0

                # Split based on orientation
                if width > height:  # Landscape (wide)
                    mid_x = x0 + width / 2

                    # Left half
                    left_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
                    left_page.merge_page(original_page)
                    left_page.cropbox.lower_left = (x0, y0)
                    left_page.cropbox.upper_right = (mid_x, y1)

                    # Right half
                    right_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
                    right_page.merge_page(original_page)
                    right_page.cropbox.lower_left = (mid_x, y0)
                    right_page.cropbox.upper_right = (x1, y1)

                else:  # Portrait (tall)
                    mid_y = y0 + height / 2

                    # Top half (left)
                    left_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
                    left_page.merge_page(original_page)
                    left_page.cropbox.lower_left = (x0, mid_y)
                    left_page.cropbox.upper_right = (x1, y1)

                    # Bottom half (right)
                    right_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
                    right_page.merge_page(original_page)
                    right_page.cropbox.lower_left = (x0, y0)
                    right_page.cropbox.upper_right = (x1, mid_y)

                # Optional rotation
                if rotate:
                    left_page.rotate(90)
                    right_page.rotate(90)

                # Store pages with their A4 page numbers
                split_pages[left_a4] = left_page
                split_pages[right_a4] = right_page

                print(f"A3 page {a3_sheet_num:2d} -> A4 pages {left_a4:2d}, {right_a4:2d}")

            # Create new PDF with pages in correct order (1, 2, 3, ...)
            pdf_writer = PyPDF2.PdfWriter()

            print(f"\nReordering pages 1-{total_pages}...")
            for page_num in range(1, total_pages + 1):
                if page_num in split_pages:
                    pdf_writer.add_page(split_pages[page_num])
                    print(f"Added A4 page {page_num}")
                else:
                    # Create blank page if missing
                    blank_page = PyPDF2.PageObject.create_blank_page(width=595, height=842)  # A4 size
                    pdf_writer.add_page(blank_page)
                    print(f"Added blank page {page_num} (missing)")

            # Write output
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"\nSuccessfully created: {output_path}")
            return str(output_path)

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main function"""

    # Parse command line options
    usage = "usage: %prog [options] <pdf filename>"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--pages", type="int", dest="pages",
                     help="Total A4 pages (auto-detect if not specified)")
    parser.add_option("-r", "--rotate", action="store_true", dest="rotate",
                     help="Rotate pages 90 degrees")
    parser.add_option("-v", "--verify", action="store_true", dest="verify",
                     help="Verify mapping formula only")

    (options, args) = parser.parse_args()

    # Verify mode
    if options.verify:
        success = verify_mapping()
        sys.exit(0 if success else 1)

    # Process PDF mode
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    input_file = args[0]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    if not input_file.lower().endswith('.pdf'):
        print("Error: Input must be a PDF file")
        sys.exit(1)

    # Process the PDF
    result = split_and_reorder_pdf(input_file, options.pages, options.rotate)

    if result:
        print(f"Success! Output saved as: {result}")
        sys.exit(0)
    else:
        print("Failed to process PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()