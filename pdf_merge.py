#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
作者：大白
时间：2020.9.16完成
功能：function
    把多个小的pdf文件，组合成一个pdf文件
参数说明：paramters description
    files_pages:        需要组合的pdf，及其指定的页码范围——"1.pdf,1,2,3,4-7;2.pdf,3,2,5-9"
    save_file_name:     组合后生成的pdf文件名

使用范例：how to use it
    python pdf_merge.py --files_pages "1,2,1_2.pdf;3,4-5,3_5.pdf;6-8,6_8.pdf" --save_file_name "pdfmerge.pdf"
'''
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse

def pdf_merger(files_pages, save_file_name):
    merge_files = files_pages.split(';')
    if '' in merge_files:       #没有if 的判断，会报错
        merge_files.remove('')  # 输入的--pages中,以";"结尾,则split后,在数组中出现最后一个为''

    pdf_writer = PdfFileWriter()

    for file_page in merge_files:
        file_page = file_page.split(',')

        file_name = file_page[0]

        pdf_reader = PdfFileReader(file_name)

        page_nums = []

        if len(file_page) == 1 or file_page[1] == "all" or file_page[1] == "":  # 如果没有指定页码，则认为该文件全部的页码
            page_nums = [num for num in range(pdf_reader.getNumPages())]
        else:
            pages = file_page[1:]
            for page in pages:
                # 注意：python下标是从0开始, 输入的页码，是从1开始
                if '-' in page:
                    page = page.split('-')
                    page = [num for num in range(int(page[0])-1, int(page[1])-1+1)]
                else:
                    page = [int(page) - 1]
                page_nums.extend(page)

        for page in page_nums:
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(save_file_name, 'wb') as out:
        pdf_writer.write(out)
        print('Created: {}'.format(save_file_name))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(usage="it's usage tip.", description="python pdf_merge.py --files_pages '1,2,3,file_name.pdf;78-98,file2_name.pdf' --save_file_name 'mergepdfs.pdf'")
    parser.add_argument("--files_pages", "-f", help="想要组合的文件及其页码，例：'1.pdf,1,2,3,4-7;2.pdf,3,2,5-9'")
    parser.add_argument("--save_file_name", "-s", help="保存成的文件名")

    args = parser.parse_args()

    files_pages = args.files_pages
    save_file_name = args.save_file_name
    
    pdf_merger(files_pages, save_file_name)