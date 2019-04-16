# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 17:03:13 2018

@author: leolqli
"""
import pandas as pd
import os 
import numpy as np


def read_file_name(filename_list, file_name_short, file_dir):
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            filename_list.append(os.path.join(root,file))
            file_name_short.append(file)
            
table_file_dir = './data/test_data2'
filename_list = []
file_name_short = []
table_file_save = open('./data/test_data2.txt', 'w')

read_file_name(filename_list, file_name_short, table_file_dir)

line_num = 0
N = 5
for file_name in filename_list:

    #get the header
    excel = pd.read_excel(file_name, header = None)
#    header_table = list(excel.columns)
#    header_table =[i.replace("\n", "").encode("utf-8") for i in header_table if type(i) == type(u'a')]
#    header_table =[''.join(i.split()) for i in header_table]
#    
#    #delete the 'Unnamed' in header 
#    header_table =[i for i in header_table if 'Unnamed' not in i]
                          
    excel = excel.fillna('')
    #save the top5 content
    content_top5 = []
    num = 0
    for index, content in excel.iterrows():
        if(num == N):
            break
        content_top5.append(content.tolist())
        num += 1
    
    #save the table and save the header
    table_file_save.write(file_name_short[line_num] + "\t")
#    table_file_save.write('#R#'.join(header_table) + "\t")
    
    num = 0
    for content in content_top5:
        content_save = []
        for i in content:
            if(type(i) == type(u'a')):
                i = ''.join(i.split())
                content_save.append(i.replace("\n", "").encode('utf-8'))
            elif(i == ''):
                continue
            else:
                content_save.append(str(i))
        
        table_file_save.write('#R#'.join(content_save))
        num += 1
        if(num != len(content_top5)):
            table_file_save.write("\t")
                              
    table_file_save.write("\n")
    
    line_num += 1
#    if(line_num)

table_file_save.close()