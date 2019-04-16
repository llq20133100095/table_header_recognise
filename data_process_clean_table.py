# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:43:07 2018

@author: leolqli
"""
import os 
import pandas as pd

def read_file_name(filename_list, file_name_short, file_dir):
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            filename_list.append(os.path.join(root,file))
            file_name_short.append(file)
            
table_file_dir = './data/clean_tables'
filename_list = []
file_name_short = []
table_file_save = open('./data/clean_table_process.txt', 'w')

read_file_name(filename_list, file_name_short, table_file_dir)

#read each table
line_num = 0
for file_name in filename_list:

    #get the header
    excel = pd.read_excel(file_name)
    header_table = list(excel.columns)
    header_table =[i.replace("\n", "").encode("utf-8") for i in header_table]
    header_table =[''.join(i.split()) for i in header_table]
    
    #save the table
#    file_name_save = file_name.split("\\")[1].replace(".xls", "")
    table_file_save.write(file_name_short[line_num] + "\t")
    table_file_save.write('#R#'.join(header_table))
    table_file_save.write("\n")
    
    print("process %d" % (line_num))
    
    line_num += 1
#    if(line_num == 29):
#        break
    
table_file_save.close()

#a='   a    b   c '
#b=''.join(a.split())