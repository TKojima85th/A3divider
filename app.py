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
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_pdf(file_stream, vertical_mode=False, rotate_mode=False):
    """
    Split A3 PDF pages into A4 pages
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
            # Get options
            vertical_mode = 'vertical' in request.form
            rotate_mode = 'rotate' in request.form

            # Process the PDF
            output_stream = split_pdf(file.stream, vertical_mode, rotate_mode)

            # Generate output filename
            original_name = Path(file.filename).stem
            output_filename = f"{original_name}_A4.pdf"

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
    app.run(debug=True, port=5000)