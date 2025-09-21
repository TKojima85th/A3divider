#!/usr/bin/env python3
import PyPDF2
from optparse import OptionParser
import sys
import re

# オプションや引数の処理
usage = "usage: /path/to/%prog [options] <pdf filename w/ .pdf>"
parser = OptionParser(usage = usage)
parser.add_option("-v", "--vertical", action="store_true", dest="vertical", help="縦書き")
parser.add_option("-r", "--rotate", action="store_true", dest="rotate", help="90度回転させる")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    sys.exit()

output_filename = re.match(r'(.*)\.pdf', args[0]).groups()[0] + '_A3toA4_v3.pdf'

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

        # ページの幅と高さを計算
        width = x1 - x0
        height = y1 - y0

        # A3横向き（横長）の場合は左右に分割
        if width > height:
            # 中央のX座標を計算
            mid_x = x0 + width / 2

            # 左半分のページ
            left_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            left_page.merge_page(original_page)
            left_page.cropbox.lower_left = (x0, y0)
            left_page.cropbox.upper_right = (mid_x, y1)

            # 右半分のページ
            right_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            right_page.merge_page(original_page)
            right_page.cropbox.lower_left = (mid_x, y0)
            right_page.cropbox.upper_right = (x1, y1)

            # オプションで90度回転
            if options.rotate:
                left_page.rotate(90)
                right_page.rotate(90)

            # 縦書きの時は右のページが先に来るようにする
            if options.vertical:
                pdf_writer.add_page(right_page)
                pdf_writer.add_page(left_page)
            else:
                # 通常は左→右の順序
                pdf_writer.add_page(left_page)
                pdf_writer.add_page(right_page)

        # A3縦向き（縦長）の場合は上下に分割
        else:
            # 中央のY座標を計算
            mid_y = y0 + height / 2

            # 上半分のページ
            top_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            top_page.merge_page(original_page)
            top_page.cropbox.lower_left = (x0, mid_y)
            top_page.cropbox.upper_right = (x1, y1)

            # 下半分のページ
            bottom_page = PyPDF2.PageObject.create_blank_page(width=width, height=height)
            bottom_page.merge_page(original_page)
            bottom_page.cropbox.lower_left = (x0, y0)
            bottom_page.cropbox.upper_right = (x1, mid_y)

            # オプションで90度回転
            if options.rotate:
                top_page.rotate(90)
                bottom_page.rotate(90)

            # 通常は上→下の順序
            pdf_writer.add_page(top_page)
            pdf_writer.add_page(bottom_page)

    # ファイルへの書き出し
    with open(output_filename, mode='wb') as f:
        pdf_writer.write(f)

print(f"Successfully created: {output_filename}")