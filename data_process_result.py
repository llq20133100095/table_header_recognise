# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 14:52:21 2018

@author: leolqli
"""
def table_content_process(table_cont):
    
    table_cont_save = []
    
    table_cont_list = table_cont.split(":")[1:]
    for lines in table_cont_list:
        table_cont_save.append(lines.split("\\n")[0])
    
    return table_cont_save


def table_save(table_name, table_cont_save, table_file_save):
    
    #have content
    if(len(table_cont_save) != 0):
        table_cont_save =[i for i in table_cont_save if i != '未命名的问题']
        
        if(len(table_cont_save) != 0):
            table_file_save.write(table_name + "\t")
            table_file_save.write('#R#'.join(table_cont_save))
            table_file_save.write("\n")


table_file = open('./data/result.txt', 'r')
table_file_save = open('./data/result_process.txt', 'w')

line_num = 0
with table_file as f:
    for lines in f.readlines():
        line_num += 1
        lines = lines.strip("\n")
        
        table_name = lines.split("$")[1].split(" ")[0]
        
        #have table content
        if(' ' in lines):
            name_cont_pos = lines.index(" ")
            table_cont = lines[name_cont_pos+1:-1]
            table_cont_save = table_content_process(table_cont)
            
            #save table
            table_save(table_name, table_cont_save, table_file_save)
            
        else:
            print "no have table contents"
        
table_file_save.close()