#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   docxWriter.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/23 14:31   gxrao      1.0         None
'''

# import lib

from docx import Document
from docx.shared import Inches
from docx.shared import Cm

document = Document()

document.add_heading('Document Title', 0)

p = document.add_paragraph('A plain paragraph having some ')
p.add_run('bold').bold = True
p.add_run(' and some ')
p.add_run('italic.').italic = True

document.add_heading('Heading, level 1', level=1)
document.add_paragraph('Intense quote', style='Intense Quote')

document.add_paragraph(
    'first item in unordered list', style='List Bullet'
)
document.add_paragraph(
    'first item in ordered list', style='List Number'
)

document.add_picture('lombplot.png', width=Cm(14.8), height = Cm(5.86))

records = (
    (3, '101', 'Spam'),
    (7, '422', 'Eggs'),
    (4, '631', 'Spam, spam, eggs, and spam')
)

table = document.add_table(rows=1, cols=3, style="Light Shading Accent 1")
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Qty'
hdr_cells[1].text = 'Id'
hdr_cells[2].text = 'Desc'
for qty, id, desc in records:
    row_cells = table.add_row().cells
    row_cells[0].text = str(qty)
    row_cells[1].text = id
    row_cells[2].text = desc

document.add_page_break()

document.save('demo.docx')


from pathlib import Path

import win32com.client as win32

def word2pdf(filedoc):
    """ convert the word *.doc, *.docx to *.pdf (save to same location)
    Args:
        filedoc (str): the file path for doc files
    """
    try:
        word = None
        doc = None
        if Path(filedoc).suffix in ['.doc', '.docx']:
            output = Path(filedoc).with_suffix('.pdf')
            if output.exists():
                return
            print("Convert WORD into PDF: "+filedoc)
            word = win32.DispatchEx('Word.Application')
            word.Visible = 0
            doc = word.Documents.Open(filedoc, False, False, True)
            # 'OutputFileName', 'ExportFormat', 'OpenAfterExport', 'OptimizeFor', 'Range',
            # 'From', 'To', 'Item', 'IncludeDocProps', 'KeepIRM', 'CreateBookmarks', 'DocStructureTags',
            # 'BitmapMissingFonts', 'UseISO19005_1', 'FixedFormatExtClassPtr'
            doc.ExportAsFixedFormat(
                str(output),
                ExportFormat=17,
                OpenAfterExport=False,
                OptimizeFor=0,
                CreateBookmarks=1)
    except Exception as e:
        print('open failed due to \n' + str(e))
    finally:
        if doc:
            doc.Close()
        if word:
            word.Quit()
word2pdf("E:\PythonWord\demo.docx")