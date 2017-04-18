# -*- coding:utf-8 -*-

import os
import shutil

FILE_DIR = '/home/lee/YEEYAN_/parser_result'
SAVE_DIR = '/home/lee/YEEYAN_/pretty_result_'

ids = []

file_list = os.listdir(FILE_DIR)

for file in file_list:
    id = file.split('_')[0]
    if id in ids:
        continue
    ids.append(id)

length = len(ids)

seg_point = length/4

for i in range(4):
	for id in ids[seg_point*i:seg_point*(i+1)]:
		save_dir = SAVE_DIR+'/'+'part_'+str(i)
		file_name_zh = str(id)+'_zh.txt'
		file_name_en = str(id)+'_en.txt'
		file_path_zh = FILE_DIR+'/'+file_name_zh
		file_path_en = FILE_DIR+'/'+file_name_en
		if os.path.exists(file_path_en) and os.path.exists(file_path_zh):				
			shutil.move(file_path_zh,save_dir)
			shutil.move(file_path_en,save_dir)

for id in ids[seg_point*4:]:
		save_dir = SAVE_DIR+'/'+'part_'+str(3)
		file_name_zh = str(id)+'_zh.txt'
		file_name_en = str(id)+'_en.txt'
		file_path_zh = FILE_DIR+'/'+file_name_zh
		file_path_en = FILE_DIR+'/'+file_name_en
		if os.path.exists(file_path_en) and os.path.exists(file_path_zh):				
			shutil.move(file_path_zh,save_dir)
			shutil.move(file_path_en,save_dir)


