#coding:utf-8
import requests
import codecs
from bs4 import BeautifulSoup
import time
import os
import random


header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
path_file = r"./amap_data.txt"
path_part = "D:\\data\\POI\\"
url_0 = "http://poi86.com/poi/amap/city/{}.html"


#
def get_html(url):
    while True:
        try:
            response = requests.get(url, headers=header, timeout=30)
            if response.status_code == 200:
                return response.content.decode()
        except Exception as e:
            print(e)
            pass


#
def main():
    with codecs.open(path_file, 'rb', 'utf-8')as fin:
        for line in fin:
            lis = line.strip().split()
            print(lis)
            try:
                do_get(lis)
            except Exception as e:
                print(e)


#
def do_get(lis):
    path = path_part + lis[0] + '//' + lis[-1] + '//'
    if not os.path.exists(path):
        os.makedirs(path)
    url = url_0.format(lis[1])
    html = get_html(url)
    res = BeautifulSoup(html, 'lxml')
    li_list = (res.find('ul', {"class": "list-group"})).find_all("li")
    for i_li in li_list:
        url_1 = (i_li.find('a')['href']).strip().split('1.html')[0] + '{}.html'
        num = (int(i_li.find('span').get_text()) // 50) + 1
        name = path + i_li.find('a').get_text() + '.txt'
        print(i_li.find('a').get_text())
        get_poi(url_1, name, num)


#
def get_poi(url, name, num):
    with codecs.open(name, 'a+', 'utf-8')as fout:
        for i in range(100):
            print(i + 1)
            url_ = ('http://poi86.com' + url).format(str(i + 1))
            html = get_html(url_)
            res = BeautifulSoup(html, 'lxml')
            tbody = res.find('table', {"class": "table table-bordered table-hover"})
            if tbody:
                print('****************')
            for i_tr in tbody.find_all('tr'):
                td_list = i_tr.find_all('td')
                if td_list:
                    fout.write("%s\t%s\t%s\t%s\n" % (td_list[0].get_text(), td_list[1].get_text(), td_list[2].get_text(), td_list[3].get_text()))
            time.sleep(random.random())


if __name__ == '__main__':
    main()
