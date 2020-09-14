#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
作者：大白
时间：2020.9.14完善
功能：function
    把目标pdf文件中的一些pages，整合出来放到一个pdf中
参数说明：paramters description
    dst_file：   要拆分的文件
    pages：      拆分文件中的页码和另存为的文件名
    save_dir:    拆分后，文件存储的路径;默认为工作目录中

使用范例：how to use it
    python pdf_split.py --dst_file "STEMI文章.pdf" --save_dir 'C:\\User\\Desktop\\pdf_split_folder' --pages "1,2,1_2.pdf;3,4-5,3_5.pdf;6-8,6_8.pdf"
'''

# import lib
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse

def pdf_splitter(dst_file, pages_file_name, save_dir):
    print(dst_file, pages_file_name, save_dir)

    """
    split pages from destination PDF file according the given parameter,pages

    command line:
    --dst_file ...pdf --pages 1,2,3,file_name.pdf;78-98,file2_name.pdf
    """
    fname = os.path.splitext(os.path.basename(dst_file))[0]
    
    #output_filename = "{}_from_{}.pdf".format(save_file,os.path.basename(dst_file))
    
    save_files = pages_file_name.split(';')
    if '' in save_files:       #没有if 的判断，会报错
        save_files.remove('')  # 输入的--pages中,以";"结尾,则split后,在数组中出现最后一个为''

    for each_save_file in save_files:
        each_page_file = each_save_file.split(',')
        file_name = os.path.join(save_dir, each_page_file[-1].strip())
        pages = each_page_file[0:-1]
        page_nums = []
        for page in pages:
            # page 只有两种形式：1,2,3,7-8,file_name.pdf
            # 即要么是数字，要么是数字-数字,这两种形式
            # 即：把目标文件的1,2,3页和7,8页,整合放入file_name.pdf中
            # 注意：python下标是从0开始, 输入的页码，是从1开始
            if '-' in page:
                page = page.split('-')
                page = [num for num in range(int(page[0])-1, int(page[1])-1+1)]
            else:
                page = [int(page)-1]
            page_nums.extend(page)

        pdf_reader = PdfFileReader(dst_file)
        pdf_writer = PdfFileWriter()
        for page in page_nums:
            pdf_writer.addPage(pdf_reader.getPage(page))
        with open(file_name, 'wb') as out :
            pdf_writer.write(out)
            print('Created: {}'.format(file_name))
if __name__ == '__main__' :
    # path = 'STEMI文章.pdf'
    #pdf_splitter(path)
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="python pdf_split.py --dst_file ...pdf --pages 1,2,3,file_name.pdf;78-98,file2_name.pdf")
    # parser.add_argument("--address", default=80, help="the port number.", dest="code_address")
    # parser.add_argument("--flag", choices=['.txt', '.jpg', '.xml', '.png'], default=".txt", help="the file type")
    # parser.add_argument("--port", type=int, required=False, help="the port number.")
    # parser.add_argument("-l", "--log", default=False, action='store_true', help="active log info.")
    parser.add_argument("--dst_file", help="想要拆分的目标文件.")
    parser.add_argument("--pages", help="想要从目标文件中提取的页数")
    parser.add_argument("--save_dir", default=os.getcwd(), help="保存文件的路径")

    args = parser.parse_args()
    dst_file = args.dst_file
    pages = args.pages  # 输入的数字，下标从1开始，需要进行相关转换
    save_dir = args.save_dir
    pdf_splitter(dst_file, pages, save_dir)
    



    
