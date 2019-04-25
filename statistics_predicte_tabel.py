# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 19:02:18 2018

@author: leolqli
"""
from collections import Counter
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix
import copy
import math
import re

def get_stat_result(result_table, clean_table, stat_file):
    """
    I count the words that often appear in the header and save them.
    
    Input:
        1.result_table: './data/result_process.txt'
        2.clean_table: './data/clean_table_process.txt'
        3.stat_file: save the 'stat_sort' file
    Return:
        1.stat_sort: a list has words and frequent. [(word1, frequent),(word2, frequent),...]
    
    """
    pattern = u'[^0-9一二三四五六七八九十\.\!\/_,$%^*(+\"\')+——()?【】“”！，。？、~@#￥%……&*（）]'
    stat_save_file = open(stat_file, 'w')
    
    statistics_dict = {}
    with open(result_table, 'r') as f:
        for lines in f.readlines():
            lines_list = lines.strip("\n").split("\t")
            
            word_list = lines_list[1].split("#R#")
            for word in word_list:
                #delete the number types
                remain_word = re.findall(pattern, word.decode('utf-8'))
                word = ''.join(remain_word).encode('utf-8')
                
                if(word in statistics_dict.keys()):
                    statistics_dict[word] += 1
                else:
                    statistics_dict[word] = 1
    
    with open(clean_table, 'r') as f:
        for lines in f.readlines():
            lines_list = lines.strip("\n").split("\t")
            
            word_list = lines_list[1].split("#R#")
            for word in word_list:
                #delete the number types
                remain_word = re.findall(pattern, word.decode('utf-8'))
                word = ''.join(remain_word).encode('utf-8')

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

    with open(stat_file, 'r+') as f:
        content = f.read()        
        f.seek(0, 0)
        f.write(str(len(statistics_dict)) + '\n' + content)
        
    return stat_sort

def statistics_dictionary(stat_file):
    line_num = 0
    stat_sort = []
    with open(stat_file, 'r') as f:
        for lines in f.readlines():
            if(line_num == 0):
                line_num += 1
                continue
            
            lines_list = lines.strip("\n").split("\t")
            
            stat_sort.append((lines_list[0], int(lines_list[1])))
            
    return stat_sort
  
def cal_header_rate(unclean_table):
    """
    Calculate the header rate in top5 rows.
    Input:
        1.unclean_table: test data
    Output:
        1.result_watch: header_rate in each file
        2.header_true: true label in test data
    """
    result_watch = []
    header_true = []
    result_num = []
    result_test_word =[]
    pattern = u'[^\.\!\/_,$%^*(+\"\')+——()?【】“”！，。？、~@#￥%……&*（）]'

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
            #top5 rows frequent
            all_frequent_num = 0.0
            all_word_in_stat_num = 0.0
            sim_rate = 0.0
            for row in lines_list[2:]:
                words = row.split("#R#")
                words = set(words)
                test_word = []
                word_in_stat_num = 0 
                
                #all rows match
                for word in words:
                    if('(' in word):
                        word = word.split("(")[0]
                    if('（' in word):
                        word = word.split("（")[0]
                    
                    #delete the punctuation
                    remain_word = re.findall(pattern, word.decode('utf-8'))
                    word = ''.join(remain_word).encode('utf-8')
                    
                    if(word in stat_sort_word):   #check if has this word
                        test_word.append(word)
                        all_word_in_stat_num += 1
                        word_in_stat_num += 1
                    
                        for (dict_word, freq) in stat_sort:
                            if(word in dict_word):
                                all_frequent_num += freq
    
                
            for row in lines_list[2:]:
                word_in_stat_num = 0 
                words = row.split("#R#")
                words = set(words)
                test_word = []
                
                #each rows match
                frequent_num = 0.0
                for word in words:
                    if('(' in word):
                        word = word.split("(")[0]
                    if('（' in word):
                        word = word.split("（")[0]
                    
                    #delete the punctuation   
                    remain_word = re.findall(pattern, word.decode('utf-8'))
                    word = ''.join(remain_word).encode('utf-8')
                    
                    if(word in stat_sort_word):   #check if has this word
                        test_word.append(word)
                        word_in_stat_num += 1
                    
                        for (dict_word, freq) in stat_sort:
                            if(word in dict_word):
                                frequent_num += freq
                            
                #calculate the header_rate
                if(frequent_num == 0):
                    sim_rate = 0.0
                else:
                    #calculate the similar rate
                    fre_rate = np.power(np.log(1 + frequent_num / all_frequent_num), 2)
                    sim_rate = float(word_in_stat_num) / len(words)
#                    print sim_rate
                    sim_rate = sim_rate * fre_rate
                    
                if(word_in_stat_num >= 2):
                    row_watch.append(sim_rate)
                else:
                    row_watch.append(0.0)
                row_num.append(len(words))
                result_test_word.append(test_word)

            result_watch.append(row_watch)
            result_num.append(row_num)
            
    return result_watch, header_true, result_test_word

def predicted_label(result_watch, threshold):
    """
    predict which row is the header
    """
    #predict 
    result_watch2 = []
    for i in range(len(result_watch)):
        temp_result_watch = []
        for j in range(len(result_watch[i])):
            if(result_watch[i][j] >= threshold):
                temp_result_watch.append((j,result_watch[i][j]))
        result_watch2.append(temp_result_watch)
    
    
    #get the max vaule
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

    return header_predicted

def precision_recall(header_true, header_predicted):
    """
    calculate the precision and recall.
    """
    con_mat = confusion_matrix(np.array(header_true), header_predicted)
    recall = 0.0
    true_num = 0.0
    for i in range(1, len(con_mat)):
        for j in range(len(con_mat[i])):
            true_num += con_mat[i][j]
        recall += con_mat[i][i]
    recall = recall / true_num
        
    precision = 0.0
    true_num = 0.0
    for i in range(0, len(con_mat)):
        for j in range(1, len(con_mat[i])):
            true_num += con_mat[i][j]
    for i in range(1, len(con_mat)):
        precision += con_mat[i][i]
        
    precision =  precision / true_num
    print ("Precision: %f" % np.mean(precision))
    print("Recall: %f" % np.mean(recall))  
        
if __name__ == '__main__':
    #threshold
    threshold = 0.125
    #"result_table" and "clean_table" are the files of reference header.
    result_table = './data/result_process.txt'
    clean_table = './data/clean_table_process.txt'
    
    #save frequent dicitionary in this file.
    stat_file = './data/statistics_word.txt'
    #test data: unclean_table_process.txt or test_data2.txt
    unclean_table = './data/unclean_table_process.txt'
    
    #get the frequent dictionary
#    stat_sort = get_stat_result(result_table, clean_table, stat_file)
    stat_sort = statistics_dictionary(stat_file)
    
    #select biggest than 2 frequent
    stat_sort = [each_stat for each_stat in stat_sort if(each_stat[1] >= 3 and each_stat[0] !='')]
    stat_sort_word = [each_stat[0] for each_stat in stat_sort]
    
    #calculate the header_rate in each unclean_table
    result_watch, header_true, result_test_word = cal_header_rate(unclean_table)
            
    #predicte the label in test data
    header_predicted = predicted_label(result_watch, threshold)
        
    #precision and recall
#    precision = precision_score(np.array(header_true), header_predicted, average=None)
#    recall = recall_score(np.array(header_true), header_predicted, average=None)
#    print ("Precision: %f" % np.mean(precision))
#    print("Recall: %f" % np.mean(recall))
    
    print confusion_matrix(np.array(header_true), header_predicted)
    precision_recall(header_true, header_predicted)