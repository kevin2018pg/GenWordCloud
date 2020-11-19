GenWordCloud, 面向本地文件, 在线网页, 程序输入的字符云自动生成组件,支持用户自定义图片字符形状, 生成给定网页,文本的高频词和关键词词云.


# 主要功能

支持三种类型的高频词和关键词可视化接口，关键词采用通用的tfidf算法提取而成。
1) show_wordcloud_online, 根据用户输入指定网址,通过采集该网址文本进行处理


```python
'''根据用户输入载入本地文本进行处理'''
def show_wordcloud_online(self, url, picturefile, words_num, save_name):
    content = self.get_webcontent(url)
    self.show_main(content, picturefile, words_num, save_name)
    return
```

2) show_wordcloud_input, 根据用户输入文本字符串进行处理

```python
'''根据用户输入文本进行处理'''
def show_wordcloud_input(self, content, picturefile, words_num, save_name):
    self.show_main(content, picturefile, words_num, save_name)
    return
```

2) show_wordcloud_offline, 根据用户输入载入本地文本进行处理, 用户将所需处理文本文件放入text文件夹中,指定文件名称进行处理

```python
'''根据用户输入url进行处理'''
def show_wordcloud_offline(self, textfile, picturefile, words_num, save_name):
    content = self.read_local_file(textfile)
    self.show_main(content, picturefile, words_num, save_name)
    return
```


# 运行方式

**参数:**
1) textfile: 放于text文件夹中, 为用户需要分析的文本
2) picturefile: 放于background文件夹中, 为用户给定的图片源文件
3) url: 用户需要进行分析网页文本的url
4) content: 用户需要分析的文本字符串
5) save_name: 用户对当前分析目标的命名
6) word_num: 用户希望展示的词数

输出: 在output文件夹下会生成以save_name开头的高频词云图和关键词云图

```python
textfile = 'beijing.txt'
picturefile = 'china.jpg'
url = 'https://news.sina.com.cn/c/2020-07-26/doc-iivhuipn5142014.shtml'
content = '''
。。。。。。。。。。。。略
'''
save_name = 'Trump'
words_num = 50
handler = CreateWordCloud()
handler.show_wordcloud_input(content, picturefile, words_num, save_name)
handler.show_wordcloud_online(url, picturefile, words_num, save_name)
handler.show_wordcloud_offline(textfile, picturefile, words_num, save_name)
```
