# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:39:24 2018

@author: leolqli
"""
from collections import Counter
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score
import copy

def get_stat_result():
    result_table = './data/result_process.txt'
    clean_table = './data/clean_table_process.txt'
    stat_save_file = open('./data/statistics_word.txt', 'w')
    
    statistics_dict = {}
    with open(result_table, 'r') as f:
        for lines in f.readlines():
            lines_list = lines.strip("\n").split("\t")
            
            word_list = lines_list[1].split("#R#")
            for word in word_list:
                if(word in statistics_dict.keys()):
                    statistics_dict[word] += 1
                else:
                    statistics_dict[word] = 1
    
    with open(clean_table, 'r') as f:
        for lines in f.readlines():
            lines_list = lines.strip("\n").split("\t")
            
            word_list = lines_list[1].split("#R#")
            for word in word_list:
                if(word in statistics_dict.keys()):
                    statistics_dict[word] += 1
                else:
                    statistics_dict[word] = 1
    
    #sort the dictionary and save this            
    stat_sort = Counter(statistics_dict).most_common()  
    
    for each_stat in stat_sort:
        if(each_stat[0] !=''):
            stat_save_file.write(each_stat[0] + "\t" + str(each_stat[1]) + "\n")
    
    stat_save_file.close()
        
    return stat_sort

"""
predict which row is the header
"""
stat_sort = get_stat_result()

#select biggest than 2 frequent
stat_sort = [each_stat[0] for each_stat in stat_sort if(each_stat[1] > 3 and each_stat[0] !='')]


unclean_table = './data/unclean_table_process.txt'
result_watch = []
header_true = []
result_num = []
result_test_word =[]
with open(unclean_table, 'r') as f:
    for lines in f.readlines():
        lines_list = lines.strip("\n").split("\t")
        
        header_true.append(int(lines_list[1]))
        
        #static the number of words in file 
        all_words_num = 0
        for row in lines_list[2:]:
            words = row.split("#R#")
            words = set(words)
            all_words_num += len(words)
            
        #recognise which row is the header
        row_watch = []
        row_num = []
        for row in lines_list[2:]:
            word_in_stat_num = 0 
            words = row.split("#R#")
            words = set(words)
            test_word = []
            for word in words:
                if('(' in word):
                    word = word.split("(")[0]
                if('（' in word):
                    word = word.split("（")[0]
                if(word in stat_sort):
                    test_word.append(word)
                    word_in_stat_num += 1
                    
            #calculate the similar rate
            sim_rate = float(word_in_stat_num) / len(words)
            if(len(words) >= 2):
                row_watch.append(sim_rate)
            else:
                row_watch.append(0.0)
            row_num.append(word_in_stat_num)
            result_test_word.append(test_word)
            
        result_watch.append(row_watch)
        result_num.append(row_num)
        
##predict
#header_predicted = []
#result_watch2 = []
#for i in range(len(result_watch)):
#    temp_result_watch = []
#    predicted_id = -1
#    for j in range(len(result_watch[i])):
#        if(result_watch[i][j] > 0.4 and j > predicted_id):
#            predicted_id = j
#            temp_result_watch.append(True)
#        else:
#            temp_result_watch.append(False)
#    result_watch2.append(temp_result_watch)
#    header_predicted.append(predicted_id)

#predict 
result_watch2 = []
for i in range(len(result_watch)):
    temp_result_watch = []
    for j in range(len(result_watch[i])):
        if(result_watch[i][j] >= 0.2):
            temp_result_watch.append((j,result_watch[i][j]))
    result_watch2.append(temp_result_watch)


header_predicted = []
for i in range(len(result_watch2)):
    if(len(result_watch2[i]) == 0):
        header_predicted.append(-1)
    else:
        each_result = []
        for j in result_watch2[i]:
            each_result.append(j[1])
        predicted_id = np.argmax(each_result)

        header_predicted.append(result_watch2[i][predicted_id][0])
        
#accuracy
#header_predicted = np.argmax(result_watch, axis = 1)
precision = precision_score(np.array(header_true), header_predicted, average=None)
recall = recall_score(np.array(header_true), header_predicted, average=None)
print np.mean(precision), np.mean(recall)