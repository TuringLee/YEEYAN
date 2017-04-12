# -*- coding:utf-8 -*-

import os
import re
import cPickle as pickle
import HTMLParser
from bs4 import BeautifulSoup

PARSED_DIR = '/home/lee/YEEYAN/data'
PARSED_SAVE_DIR = '/home/lee/YEEYAN/parser_result'

parser = HTMLParser.HTMLParser()

pattern_tags = re.compile('</?span.*?>|</?b>|</?strong>|</?font.*?>|</?em>|</?a.*?>|</?u>')
pattern_space = re.compile('&nbsp')
pattern_annotations = re.compile('\[.*?\]')
pattern_bra = re.compile(u'\(.*?\)|（.*?）')


def parse_row(row):
    article_id = row[0]
    translation_content = row[1]
    original_content = row[2]

    paras_zh = parse_html(translation_content)
    paras_en = parse_html(original_content)
    zh_path = os.path.join(PARSED_SAVE_DIR, str(article_id)+'_zh.txt')
    en_path = os.path.join(PARSED_SAVE_DIR, str(article_id)+'_en.txt')
    save_parse(zh_path, paras_zh, article_id)
    save_parse(en_path, paras_en, article_id)

def save_parse(path, paras, article_id):
    if os.path.exists(path):
        os.remove(path)
    try:
        with open(path, 'a+') as fw:
            fw.writelines(paras)
    except IOError:
        print 'open file {} error!'.format(article_id)


def parse_html(html):
    html = re.sub(pattern_space, '', html)
    html = decode_html_entities(html)
    html = re.sub(pattern_tags, '', html)
    html = re.sub(pattern_annotations, u'', html)
    html = re.sub(pattern_bra, u'', html)
    paras = get_paras(html)
    return paras

def decode_html_entities(text):
    return parser.unescape(text)

def get_paras(html):
    soup = BeautifulSoup(html)
    paras = soup.get_text('\n')
    paras = paras.encode('utf8')
    paras = paras.split('\n')
    t = []
    for para in paras:
        if para.strip():
            t.append(str(para.strip())+'\n')
    return t


# main field
if __name__ == '__main__':

    ids = []

    file_list = os.listdir(PARSED_DIR)

    for file in file_list:
        id = file.split('_')[0]
        if id in ids:
            continue
        ids.append(id)


    print "parser now..."

    for i,id in enumerate(ids):
        
        file_path_zh = os.path.join(PARSED_DIR,str(id)+'_zh.txt')
        file_path_en = os.path.join(PARSED_DIR,str(id)+'_en.txt')

        if not ( os.path.exists(file_path_zh) and os.path.exists(file_path_en) ):
            continue

        f1 = open(file_path_zh)
        f2 = open(file_path_en)

        row = (id,f1.read().decode('utf8'),f2.read().decode('utf8'))

        f1.close()
        f2.close()

        parse_row(row)

        if i % 100 ==0:
            print str(i)+' files has been parsered!'

    print 'ALL DONE'