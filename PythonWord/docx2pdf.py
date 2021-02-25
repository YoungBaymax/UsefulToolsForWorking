#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   docx2pdf.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/24 18:13   gxrao      1.0         None
'''

# import lib
import os
import sys

def word2pdf(filedoc):
    if sys.platform == "win32":
        import win32com.client as win32
        from pathlib import Path
        """ convert the word *.doc, *.docx to *.pdf (save to same location)
        Args:
            filedoc (str): the file path for doc files
        """
        try:
            word = None
            doc = None
            if Path(filedoc).suffix in ['.doc', '.docx']:
                output = Path(filedoc).with_suffix('.pdf')
                # if output.exists():
                #     os.remove(output)
                print("Convert WORD into PDF: " + filedoc)
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

    elif sys.platform[:5] == 'linux':
        end_length = len(filedoc.split('.')[-1]) + 1
        name = filedoc[0:-end_length]

        cmd = 'libreoffice  --convert-to pdf  %s' % filedoc
        os.system(cmd)
        name = name.split('/')[-1] + '.pdf'
        print(name)