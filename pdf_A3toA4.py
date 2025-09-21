#!/usr/bin/env python3
import PyPDF2
from optparse import OptionParser
import sys
import re
import copy

ROTATE_ANGLE = 90

# オプションや引数の処理
usage = "usage: /path/to/%prog [options] <pdf filename w/ .pdf>"
parser = OptionParser(usage = usage)
parser.add_option("-v", "--vertical", action="store_true", dest="vertical", help="縦書き")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    sys.exit()

output_filename = re.match(r'(.*)\.pdf', args[0]).groups()[0] + '_cut.pdf'

# ファイルを開く
pdf_reader = PyPDF2.PdfFileReader(args[0])
pdf_writer = PyPDF2.PdfFileWriter()

# ページの大きさを取得する
page = pdf_reader.getPage(0)
(x0, y0) = page.mediaBox.getLowerLeft()
(x1, y1) = page.mediaBox.getUpperRight()

# 見開き1ページずつ処理をしていく
for i in range(pdf_reader.getNumPages()):
    # 半分のサイズを抽出する(p1が左，p2が右のページ)
    p1 = pdf_reader.getPage(i)
    p2 = copy.copy(p1)
    p1.cropBox.lowerLeft = (x0, y0)
    p1.cropBox.upperRight = (x1, (y0 + y1) / 2)
    p2.cropBox.lowerLeft = (x0, (y0 + y1) / 2)
    p2.cropBox.upperRight = (x1, y1)
    
    # 縦書きの時は右のページが先に来るようにする
    if options.vertical is True:
        p1, p2 = p2, p1
    
    # 時計回りに90度回転させる
    p1.rotateClockwise(ROTATE_ANGLE)
    p2.rotateClockwise(ROTATE_ANGLE)

    # PDFの再構成
    pdf_writer.addPage(p1)
    pdf_writer.addPage(p2)

# ファイルへの書き出し
with open(output_filename, mode='wb') as f:
    pdf_writer.write(f)