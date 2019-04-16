# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 17:37:13 2018

@author: leolqli
"""

import pandas as pd
import os 
import numpy as np
from statistics_table2 import get_stat_result

def read_file_name(filename_list, file_name_short, file_dir):
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            filename_list.append(os.path.join(root,file))
            file_name_short.append(file)
            
table_file_dir = 'E:/tencent_work/table_header_recognise/clean_tables'
filename_list = []
file_name_short = []

read_file_name(filename_list, file_name_short, table_file_dir)

#select biggest than 2 frequent
stat_sort = get_stat_result()
stat_sort = [each_stat for each_stat in stat_sort if(each_stat[1] > 3 and each_stat[0] !='')]
stat_sort_word = [each_stat[0] for each_stat in stat_sort]

line_num = 0
N = 6
result_watch = []
for file_name in filename_list:

    #get the header
    excel = pd.read_excel(file_name, header = None)
                          
    excel = excel.fillna('')
    #save the top5 content
    content_top5 = []
    num = 0
    for index, content in excel.iterrows():
        if(num == N):
            break
        if(num == 0):
            num += 1
            continue
        content_top5.append(content.tolist())
        num += 1
    
    
    num = 0
    row_watch = []
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
        
        #calculate the match in 
        word_in_stat_num = 0.0
        for word in content_save:
            if(word in stat_sort_word):   #check if has this word
                word_in_stat_num += 1            
        sim_rate = float(word_in_stat_num) / len(content_save)
        if(len(content_save) >= 2):
            row_watch.append(sim_rate)
        else:
            row_watch.append(0.0)
        
    result_watch.append(row_watch)
    
    line_num += 1
#    if(line_num == 1):
#        break
