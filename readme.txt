一、data
1.result.txt：用来生成result_process.txt
	file_name "\t" 表头

2.result_process.txt：从result.txt提取整合表头所生成的
	file_name "\t" 表头

3.clean_table_process.txt：已经处理好的，第一行即为表头的。
	file_name "\t" 表头

4.statistics_word.txt：从.result_process.txt和clean_table_process.txt统计表头词语的频率
	
5.unclean_table_process.txt：人为标注的，用来进行测试的数据test_data1
	file_name "\t" 第几行是表头 "\t" 展示前5行（用"\t"隔开）

6.statistics.txt：
	file_name "\t" true_label "\t" predicted_label "\t" 展示前5行的词语在字典中的相似度

7.test_data2.txt：真实场景中的数据测试test_data2

8.clean_unclean_test_test2_data.zip：解压文件夹，包含了文件夹clean_tables, unclean_tables, test_data和test_data2

二、程序
1.statistics_predicte_tabel.py：测试用的主程序，用来通过规则计算表头在哪一行。

2.statistics_table.py：这是测试用的第一版本，已经抛弃的

#####数据处理程序#######
3.null_header_generate.py：用来生成无表头的数据表格

4.data_process_clean_table.py：处理文件夹clean_table，并生成文件clean_table_process.txt

5.data_process_result.py：处理文件result.txt，并生成文件result_process.txt

6.data_process_unclean_table.py：处理文件夹unclean_tables, test_data和test_data2.
用来生成文件unclean_table_process.txt, test_data.txt和test_data2.txt