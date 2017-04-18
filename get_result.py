# -*- coding:utf-8 -*-

import os
import re
from difflib import SequenceMatcher
import argparser

pattern_punc_zh = re.compile(u'[。？！，、：；“”‘’（）——……—·《》]*')
pattern_punc_en = re.compile(u'[\?!,:;\-\.\'\"]*')
pattern_punc_zh_s = re.compile(u'^[。？！，、：；“”‘’（）——……—·《》]*')
pattern_punc_en_s = re.compile(u'^[\?!,:;\-\.\'\"]*')
pattern_dot = re.compile('@\$')

parser = argparse.ArgumentParser()
parser.add_argument('input_file_path')
parser.add_argument('output_file_path')
args = parser.parse_args()
FILE_DIR = args.input_file_path
SAVE_DIR = args.output_file_path

file_list = os.listdir(FILE_DIR)

ids = []

STATISTICS = []

for file in file_list:
    id = file.split('_')[0]
    if id in ids:
        continue
    ids.append(id)

count_sent = 0
count_para = 0
num_sent_matched = 0
num_para_matched = 0

for i_,id in enumerate(ids):
    t_st = []
    t_st.append(id)
    sent_zh = []
    sent_en = []
    num_sent_zh = []
    num_sent_en = []
    file_name_zh = str(id)+'_zh.txt'
    file_name_en = str(id)+'_en.txt'
    file_path_zh = os.path.join(FILE_DIR,file_name_zh)
    file_path_en = os.path.join(FILE_DIR,file_name_en)
    if not ( os.path.exists(file_path_zh) and os.path.exists(file_path_en) ):
        continue
    f_zh = open(file_path_zh)
    f_en = open(file_path_en)
    content_zh = f_zh.read()
    content_zh = re.sub(pattern_dot, '.', content_zh)
    content_en = f_en.read()
    f_zh.close()
    f_en.close()
    
    lines_zh = content_zh.split('\n\n')
    lines_en = content_en.split('\n\n')
    t_st.append(len(lines_zh))
    count_para += len(lines_zh)
    t_sent = 0

    for lines in lines_zh:
        tzh_lines = []
        tzh_num = 0
        lines = lines.strip().split('\n')
        if not lines[-1]:
            continue
        for line in lines[0:-1]:
            t_line = re.sub(pattern_punc_zh,'',line.decode('utf8'))
            if t_line.strip():
            	line = re.sub(pattern_punc_zh_s, '', line)
                tzh_lines.append(line)
                tzh_num += 1
        if tzh_num < 1:
            continue
        num_sent_zh.append(tzh_num)
        sent_zh.append(tzh_lines)
        count_sent += tzh_num
        t_sent += tzh_num
    t_st.append(t_sent)
    
    for lines in lines_en:
        t_lines = []
        t_num = 0
        ten_lines = []
        ten_num = 0
        lines = lines.strip().split('\n')
        if not lines[-1]:
            continue
        for line in lines[0:-1]:
            t_line = re.sub(pattern_punc_en, '', line)
            if t_line.strip():
            	line = re.sub(pattern_punc_en_s, '', line)
                t_lines.append(line)
                t_num += 1
        if t_num == 1:
        	num_sent_en.append(t_num)
        	sent_en.append(t_lines)
        	continue
        elif t_num == 0:
        	continue
        else:
        	pre_line = t_lines[0]
	        for m in range(len(t_lines)):
	        	if m == 0:
	        		continue
	        	if t_lines[m].split()[0].islower():
	        		pre_line = pre_line +' '+ line
	        	else:
	        		ten_lines.append(pre_line)
	        		ten_num += 1
	        		pre_line = t_lines[m]
	        ten_lines.append(pre_line)
	        ten_num += 1
        num_sent_en.append(ten_num)
        sent_en.append(ten_lines)

    sent_matched = SequenceMatcher(None,num_sent_en,num_sent_zh)
    matched_blocks = sent_matched.get_matching_blocks()

    matched_zh = []
    matched_en = []
    al_para = 0
    al_sent = 0
    for item in matched_blocks:
        item = tuple(item)
        a = item[0]
        b = item[1]
        c = item[2]
        al_para += c 
        '''
        size_1_path = '/home/lee/YEEYAN_/final_result/size_1.txt'
        
        if c == 1:

            f = open(size_1_path,'a+')
            f.write(str(id)+':\n') 
            f.write(str(b)+' _ '+str(num_sent_zh[b])+'\n')
            f.writelines(sent_zh[b])
            f.write('\n')
            f.writelines('-'*66+'\n')
            f.write(str(a)+' _ '+str(num_sent_en[a])+'\n')
            f.writelines(sent_en[a])
            f.write('\n\n')
            f.close()
        '''


        if c <= 1:
            continue

        
        for i in range(c):
            num_para_matched += 1
            num_sent_matched += num_sent_zh[b+i]
            al_sent += num_sent_zh[b+i]
            if (num_sent_zh[b:b+c].count(1) >= c*0.6):
            	continue
            for j in range(len(sent_zh[b+i])):
            	s_zh = sent_zh[b+i][j]
            	s_en = sent_en[a+i][j]
            	l_zh = (len(s_zh)-1)*1./3
            	l_en = len(s_en.split())
            	if l_zh <= l_en*2 and l_zh > l_en*1.3:
            		matched_zh.append(s_zh.strip()+'\n')
            		matched_en.append(s_en.strip()+'\n')
            '''		
            for sent in sent_zh[b+i]:
                matched_zh.append(sent.strip()+'\n')
            for sent in sent_en[a+i]:
                matched_en.append(sent.strip()+'\n')
            '''

    t_st.append(al_para)
    t_st.append(al_sent)
    t_st.append(matched_blocks[0:-1])
    STATISTICS.append(t_st)

    if not(matched_en and matched_zh):
        continue
    save_path_zh = os.path.join(SAVE_DIR,file_name_zh)
    save_path_en = os.path.join(SAVE_DIR,file_name_en)

    f_zh = open(save_path_zh,'a+')
    f_en = open(save_path_en,'a+')

    f_zh.writelines(matched_zh)
    f_en.writelines(matched_en)

    f_zh.close()
    f_en.close()

    if i_ % 100 == 0:
        print str(i_)+' files has been aligned'

print count_sent 
print count_para 
print num_sent_matched 
print num_para_matched 
print 'DOWN'

'''
for item in STATISTICS:
    print item
'''