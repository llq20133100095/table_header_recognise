һ��data
1.result.txt����������result_process.txt
	file_name "\t" ��ͷ

2.result_process.txt����result.txt��ȡ���ϱ�ͷ�����ɵ�
	file_name "\t" ��ͷ

3.clean_table_process.txt���Ѿ�����õģ���һ�м�Ϊ��ͷ�ġ�
	file_name "\t" ��ͷ

4.statistics_word.txt����.result_process.txt��clean_table_process.txtͳ�Ʊ�ͷ�����Ƶ��
	
5.unclean_table_process.txt����Ϊ��ע�ģ��������в��Ե�����test_data1
	file_name "\t" �ڼ����Ǳ�ͷ "\t" չʾǰ5�У���"\t"������

6.statistics.txt��
	file_name "\t" true_label "\t" predicted_label "\t" չʾǰ5�еĴ������ֵ��е����ƶ�

7.test_data2.txt����ʵ�����е����ݲ���test_data2

8.clean_unclean_test_test2_data.zip����ѹ�ļ��У��������ļ���clean_tables, unclean_tables, test_data��test_data2

��������
1.statistics_predicte_tabel.py�������õ�����������ͨ����������ͷ����һ�С�

2.statistics_table.py�����ǲ����õĵ�һ�汾���Ѿ�������

#####���ݴ������#######
3.null_header_generate.py�����������ޱ�ͷ�����ݱ��

4.data_process_clean_table.py�������ļ���clean_table���������ļ�clean_table_process.txt

5.data_process_result.py�������ļ�result.txt���������ļ�result_process.txt

6.data_process_unclean_table.py�������ļ���unclean_tables, test_data��test_data2.
���������ļ�unclean_table_process.txt, test_data.txt��test_data2.txt