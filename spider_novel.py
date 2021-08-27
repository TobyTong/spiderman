from bs4 import BeautifulSoup
import requests
import sys


class DownloadNovel(object):

    def __init__(self):
        self.domain = "https://www.bqktxt.com"
        self.target = "https://www.bqktxt.com/10_10643/"
        self.chapters = []  # 章节
        self.links = []     # 链接
        self.nums = 0       # 章节数

    '''
    获取下载链接
    '''
    def get_download_links(self):
        req = requests.get(self.target)
        req.encoding = 'GBK'
        html = req.text
        bs = BeautifulSoup(html, 'html.parser')
        div_texts = bs.findAll('div', class_='listmain')
        str_div_texts = BeautifulSoup(str(div_texts[0]), "html.parser").findAll('a')
        self.nums = len(str_div_texts[12:])
        for each in str_div_texts[12:]:
            self.chapters.append(each.string)
            self.links.append(self.domain + each.get('href'))

    '''
    获取文章内容
    '''
    def get_contents(self, target):
        req = requests.get(target)
        req.encoding = 'GBK'
        html = req.text
        bs = BeautifulSoup(html, 'html.parser')
        div_texts = bs.findAll('div', class_='showtxt')
        div_texts = div_texts[0].text.replace('－'*41, '\n\n').replace('　'*2, '\n\n')
        return div_texts

    '''
    下载后写入文件
    '''
    def writer(self, chapters, links, text):
        # write_flag = True
        with open(links, 'a', encoding='utf-8') as f:
            f.write(chapters + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    dn = DownloadNovel()
    dn.get_download_links()
    print('开始下载：')
    for i in range(dn.nums):
        dn.writer(dn.chapters[i], '斗罗大陆III龙王传说.txt', dn.get_contents(dn.links[i]))
        sys.stdout.write(" 已下载:%.3f%%" % float(i / dn.nums) + '\r')
        sys.stdout.flush()
    print('下载完成')
