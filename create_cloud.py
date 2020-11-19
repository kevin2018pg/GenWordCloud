# -*- coding: utf-8 -*-
# @Time : 2020/7/19 14:21
# @Author : Chendong
# @Email : chendong@qiyunhj.com
# @IDE: PyCharm
# @ModuleName : create_cloud
# @Description: 生成词云图current

import os
import matplotlib.pyplot as plt
from keywords_tfidf import *
from collections import Counter
import jieba.posseg as pseg
import urllib.request
from wordcloud import WordCloud, ImageColorGenerator
from newspaper import Article
import numpy as np
from PIL import Image
import requests


class CreateWordCloud:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 存放本地文本文档
        self.textdir = os.path.join(cur, 'text')
        # 存放词云图形状背景
        self.background = os.path.join(cur, 'background')
        # 词云图中文字体
        self.fontpath = os.path.join(cur, 'data/simhei.ttf')
        # 输出文件夹
        self.outpath = os.path.join(cur, 'output')
        # 词性
        self.pos_filters = ['n', 'v', 'a']
        self.limit_words = 100
        # 获取关键词对象
        self.Keyworder = TFIDF()
        return

    '''获取搜索页'''

    def get_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        # req = urllib.request.Request(url, headers=headers)
        # html = urllib.request.urlopen(req).read().decode('utf-8')
        # 获取网页字符串
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        return html

    '''读取本地文件进行处理'''

    def read_local_file(self, textfile):
        textpath = os.path.join(self.textdir, textfile)
        content = open(textpath, encoding='utf-8').read()
        return content

    '''统计词频'''

    def extract_words(self, content):
        words = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            words += [w.word for w in pseg.cut(line) if w.flag[0] in self.pos_filters and len(w.word) > 1]
        # 对列表计数，返回词频最高的的n个元素的元组，组合成字典
        word_dict = {i[0]: i[1] for i in Counter(words).most_common()}
        return word_dict

    '''抽取关键词'''

    def extract_keywords(self, content, words_num=20):
        keywords_dict = {}
        keywords = self.Keyworder.extract_keywords(content, words_num)
        for key in keywords:
            word = key[0]
            value = int(key[1] * 1000)
            keywords_dict[word] = value
        return keywords_dict

    '''创建关键词云图'''

    def show_cloud(self, word_dict, max_words, picturefile, save_name):
        self.backimage = os.path.join(self.background, picturefile)
        saveimage = os.path.join(self.outpath, save_name + '.jpg')
        # backgroud_Image = plt.imread(self.backimage)
        backgroud_Image = np.array(Image.open(self.backimage))
        cloud = WordCloud(font_path=self.fontpath,
                          background_color='white',
                          width=800,
                          height=600,
                          max_words=max_words,
                          max_font_size=500,
                          mask=backgroud_Image,
                          contour_color='steelblue',
                          random_state=44
                          )

        word_cloud = cloud.generate_from_frequencies(word_dict)
        img_colors = ImageColorGenerator(backgroud_Image)
        word_cloud.recolor(color_func=img_colors)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.savefig(saveimage)
        # plt.show()
        # plt.close()

    '''展示关键词云图'''

    def show_keywords(self, content, picturefile, words_num=20, save_name='test'):
        keywords_text = self.extract_keywords(content, words_num)
        self.show_cloud(keywords_text, words_num, picturefile, save_name)
        return

    '''展示高频词云图'''

    def show_topwords(self, content, picturefile, words_num=50, save_name='test'):
        topwords_text = self.extract_words(content)
        self.show_cloud(topwords_text, words_num, picturefile, save_name)
        return

    '''在线模式抓取新闻进行既定形状可视化'''

    def get_webcontent(self, url):
        news = Article(url, language='zh')
        news.download()
        news.parse()
        content = news.text
        return content

    '''根据用户输入url进行处理'''

    def show_wordcloud_online(self, url, picturefile, words_num, save_name):
        content = self.get_webcontent(url)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入文本进行处理'''

    def show_wordcloud_input(self, content, picturefile, words_num, save_name):
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入载入本地文本进行处理'''

    def show_wordcloud_offline(self, textfile, picturefile, words_num, save_name):
        content = self.read_local_file(textfile)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''分别执行绘制关键词和高频词'''

    def show_main(self, content, picturefile, words_num, save_name):
        name = save_name + '-topwords'
        print('正在生成该文本的高频词云图.....')
        self.show_topwords(content, picturefile, words_num, name)
        print('已完成该文本的高频词云图.....')
        print('正在生成该文本的关键词云图.....')
        name = save_name + '-keywords'
        self.show_keywords(content, picturefile, words_num, name)
        print('已完成该文本的关键词云图.....')


def test():
    # 背景图
    picturefile = 'Trump.png'
    # 用户输入
    # content = '''
    # 。。。略
    #     '''
    # 本地文本文档
    # textfile = 'beijing.txt'
    # 网页url
    url = 'https://news.sina.com.cn/c/2020-07-26/doc-iivhuipn5142014.shtml'
    # 参数，构建词云图类
    save_name = 'Trump'
    words_num = 50
    handler = CreateWordCloud()
    # handler.show_wordcloud_input(content, picturefile, words_num, save_name)
    handler.show_wordcloud_online(url, picturefile, words_num, save_name)
    # handler.show_wordcloud_offline(textfile, picturefile, words_num, save_name)


if __name__ == '__main__':
    test()
