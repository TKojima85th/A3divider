#!/usr/bin/env python3
"""
A3 to A4 PDF Splitter Web Application
"""
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import PyPDF2
import os
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Production settings
if os.environ.get('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def split_pdf_simple(file_stream, vertical_mode=False, rotate_mode=False):
    """
    Split A3 PDF pages into A4 pages (Simple Mode - Phase 1)
    """
    pdf_reader = PyPDF2.PdfReader(file_stream)
    pdf_writer = PyPDF2.PdfWriter()

    # Process each page
    for i in range(len(pdf_reader.pages)):
        original_page = pdf_reader.pages[i]

        # Get page dimensions
        mediabox = original_page.mediabox
        x0, y0 = float(mediabox.lower_left[0]), float(mediabox.lower_left[1])
        x1, y1 = float(mediabox.upper_right[0]), float(mediabox.upper_right[1])

        # Calculate width and height
        width = x1 - x0
        height = y1 - y0

        # A3 landscape (wide) - split left and right
        if width > height:
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

            # Optional rotation
            if rotate_mode:
                left_page.rotate(90)
                right_page.rotate(90)

            # Page order
            if vertical_mode:
                pdf_writer.add_page(right_page)
                pdf_writer.add_page(left_page)
            else:
                pdf_writer.add_page(left_page)
                pdf_writer.add_page(right_page)

        # A3 portrait (tall) - split top and bottom
        else:
            mid_y = y0 + height / 2

            # Top half
            top_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            top_page.merge_page(original_page)
            top_page.cropbox.lower_left = (x0, mid_y)
            top_page.cropbox.upper_right = (x1, y1)

            # Bottom half
            bottom_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            bottom_page.merge_page(original_page)
            bottom_page.cropbox.lower_left = (x0, y0)
            bottom_page.cropbox.upper_right = (x1, mid_y)

            # Optional rotation
            if rotate_mode:
                top_page.rotate(90)
                bottom_page.rotate(90)

            pdf_writer.add_page(top_page)
            pdf_writer.add_page(bottom_page)

    # Write to bytes
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

def split_pdf_booklet(file_stream, total_pages=None, rotate_mode=False):
    """
    Split A3 PDF and reorder pages according to booklet pattern (Booklet Mode - Phase 2)
    """
    pdf_reader = PyPDF2.PdfReader(file_stream)
    num_a3_pages = len(pdf_reader.pages)

    # Auto-detect total pages if not specified
    if total_pages is None:
        total_pages = num_a3_pages * 2

    # Generate mapping
    mapping = generate_booklet_mapping(total_pages)

    # Split and collect all A4 pages first
    split_pages = {}  # {A4_page_number: PageObject}

    for a3_idx in range(num_a3_pages):
        if a3_idx >= len(mapping):
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
        if rotate_mode:
            left_page.rotate(90)
            right_page.rotate(90)

        # Store pages with their A4 page numbers
        split_pages[left_a4] = left_page
        split_pages[right_a4] = right_page

    # Create new PDF with pages in correct order (1, 2, 3, ...)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(1, total_pages + 1):
        if page_num in split_pages:
            pdf_writer.add_page(split_pages[page_num])
        else:
            # Create blank page if missing
            blank_page = PyPDF2.PageObject.create_blank_page(width=595, height=842)  # A4 size
            pdf_writer.add_page(blank_page)

    # Write to bytes
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file was uploaded
    if 'file' not in request.files:
        flash('ファイルが選択されていません', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('ファイルが選択されていません', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        try:
            # Get processing mode
            processing_mode = request.form.get('mode', 'simple')
            vertical_mode = 'vertical' in request.form
            rotate_mode = 'rotate' in request.form

            # Generate output filename based on mode
            original_name = Path(file.filename).stem

            if processing_mode == 'booklet':
                # Phase 2: Booklet mode
                total_pages = request.form.get('total_pages')
                if total_pages:
                    try:
                        total_pages = int(total_pages)
                        if total_pages <= 0:
                            raise ValueError("ページ数は正の数である必要があります")
                    except ValueError as e:
                        flash(f'ページ数エラー: {str(e)}', 'error')
                        return redirect(url_for('index'))
                else:
                    total_pages = None  # Auto-detect

                output_stream = split_pdf_booklet(file.stream, total_pages, rotate_mode)
                output_filename = f"{original_name}_booklet_reordered.pdf"

            else:
                # Phase 1: Simple mode (default)
                output_stream = split_pdf_simple(file.stream, vertical_mode, rotate_mode)
                output_filename = f"{original_name}_simple_split.pdf"

            return send_file(
                output_stream,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=output_filename
            )

        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('index'))

    flash('PDFファイルのみアップロード可能です', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)