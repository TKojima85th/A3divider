#!/usr/bin/env python3
import PyPDF2
from optparse import OptionParser
import sys
import re

ROTATE_ANGLE = 90

# オプションや引数の処理
usage = "usage: /path/to/%prog [options] <pdf filename w/ .pdf>"
parser = OptionParser(usage = usage)
parser.add_option("-v", "--vertical", action="store_true", dest="vertical", help="縦書き")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    sys.exit()

output_filename = re.match(r'(.*)\.pdf', args[0]).groups()[0] + '_A3toA4_v2.pdf'

# ファイルを開く
with open(args[0], 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_writer = PyPDF2.PdfWriter()

    # 見開き1ページずつ処理をしていく
    for i in range(len(pdf_reader.pages)):
        # 元のページを取得
        original_page = pdf_reader.pages[i]

        # ページの大きさを取得する
        mediabox = original_page.mediabox
        x0, y0 = float(mediabox.lower_left[0]), float(mediabox.lower_left[1])
        x1, y1 = float(mediabox.upper_right[0]), float(mediabox.upper_right[1])

        # 左半分のページ (p1)
        p1 = PyPDF2.PageObject.create_blank_page(width=x1-x0, height=y1-y0)
        p1.merge_page(original_page)
        p1.cropbox.lower_left = (x0, y0)
        p1.cropbox.upper_right = (x1, (y0 + y1) / 2)

        # 右半分のページ (p2)
        p2 = PyPDF2.PageObject.create_blank_page(width=x1-x0, height=y1-y0)
        p2.merge_page(original_page)
        p2.cropbox.lower_left = (x0, (y0 + y1) / 2)
        p2.cropbox.upper_right = (x1, y1)

        # 縦書きの時は右のページが先に来るようにする
        if options.vertical is True:
            p1, p2 = p2, p1

        # 時計回りに90度回転させる
        p1.rotate(ROTATE_ANGLE)
        p2.rotate(ROTATE_ANGLE)

        # PDFの再構成
        pdf_writer.add_page(p1)
        pdf_writer.add_page(p2)

    # ファイルへの書き出し
    with open(output_filename, mode='wb') as f:
        pdf_writer.write(f)

print(f"Successfully created: {output_filename}")