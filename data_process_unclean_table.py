# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 17:03:13 2018

@author: leolqli
"""
import pandas as pd
import os 
import numpy as np
import time 

def read_file_name(filename_list, file_name_short, file_dir):
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            filename_list.append(os.path.join(root,file))
            file_name_short.append(file)
            
table_file_dir = u'./data/test_data'
filename_list = []
file_name_short = []
table_file_save = open(u'./data/test_data.txt', 'w')
start_time = time.time()

read_file_name(filename_list, file_name_short, table_file_dir)

line_num = 0
#save the top5 line in one excel
N = 5
for file_name in filename_list:

    #get the header
    try:
        excel = pd.read_excel(file_name, header = None)
        
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
        
        if(line_num % 50 == 0):
            print("process the %d line_num, use the time %f s" % (line_num, time.time() - start_time))
        
    except:
        line_num += 1
        print("error file name:" + file_name)
        
table_file_save.close()