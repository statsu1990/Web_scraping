import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

class WebScraping:
    def __init__(self):
        return

    @staticmethod
    def make_output_dir(base_dir_name=os.path.join('.','result'), dir_name='result', with_datetime=True):
        '''
        make output directory
        return output direcotry path
        '''
        dir_path = dir_name
        if with_datetime:
            dir_path = dir_path + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        dir_path = os.path.join(base_dir_name, dir_path)

        #
        os.makedirs(dir_path, exist_ok=True)

        return dir_path

    @staticmethod
    def get_html(url):
        res = requests.get(url)
        try:
            html = res.text
        except:
            print(' raise error in WebScraping.get_html(). status {0}.'.format(res.status_code))
            html = ''

        return html

    @staticmethod
    def get_soup_obj(url):
        html = WebScraping.get_html(url)
        soup = bs(html, 'html.parser')
        return soup

    @staticmethod
    def get_texts_in_class(soup, class_name):
        '''
        return text in class_name
        '''
        elements = soup.find_all(class_=class_name)
        #
        texts = []
        for e in elements:
            texts.append(e.string)
        return texts

    @staticmethod
    def get_texts_in_class2(soup, class_name1, class_name2, all=True):
        '''
        return text in class_name2 in class_name1
        '''
        elements = soup.find_all(class_=class_name1)
        #
        texts = []
        for e in elements:
            if all:
                elements2 = e.find_all(class_=class_name2)
            else:
                elements2 = e.find(class_=class_name2)
            for e2 in elements2:
                texts.append(e2.string)
        return texts

    @staticmethod
    def get_text_in_property(soup, property_name):
        elements = soup.find_all(property=property_name)
        #
        texts = []
        for e in elements:
            texts.append(e.string)
        return texts

    @staticmethod
    def get_href_in_class(soup, class_name):
        elements = soup.select('.' + class_name)
        #
        texts = []
        for e in elements:
            texts.append(e.get('href'))
        return texts

    @staticmethod
    def delete_brank_linefeed_in_str(string):
        return string.strip()


    def test1(self):
        #url
        #url = "https://tonari-it.com/python-html-tag-list-bs4/"
        url = "https://www.yomiuri.co.jp/"

        #get html
        html = WebScraping.get_html(url)

        #set BueatifulSoup
        soup = bs(html, "html.parser")
        
        #title
        print(soup.title)

        #
        elems = soup.select('h3 a')
        for e in elems:
            print(e)

        #
        #txt = elems.getText()
        for e in elems:
            print(e.getText())

        #
        for e in elems:
            print(e.get('href'))

        #<span id="toc4">欲しいHTML要素のouterHTMLをコピーする</span>

        #<h3><span id="toc4">欲しいHTML要素のouterHTMLをコピーする</span></h3>

        #<h3 class="home-main-photo-digital-list-item__title">
        #            <a href="http://www.yomiuri.co.jp/s/ims/lensboutyoutei/">震災8年　ＬＥＮＳ　防潮堤とともに</a>
        #          </h3>

        return

    def test2(self):
        date = 190317
        url = 'https://tabelog.com/aichi/A2301/rstLst/ramen/1/?Srt=D&SrtT=rt&sort_mode=1&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3&svd=' + str(date) + '&svt=1900&svps=2&select_sort_flg=1'

        #soup object
        soup = WebScraping.get_soup_obj(url)

        #rank
        ranks = WebScraping.get_texts_in_class(soup, 'list-rst__rank-no')
        print(ranks)

        #restaurant name
        names = WebScraping.get_texts_in_class(soup, 'list-rst__rst-name-target')
        #<a class="list-rst__rst-name-target cpy-rst-name js-ranking-num" target="_blank" data-list-dest="item_top" data-ranking="2" href="https://tabelog.com/aichi/A2301/A230110/23050032/">からみそラーメン ふくろう 本店</a>
        print(names)

        #URL
        urls = WebScraping.get_href_in_class(soup, 'list-rst__rst-name-target')
        #<a class="list-rst__rst-name-target cpy-rst-name js-ranking-num" target="_blank" data-list-dest="item_top" data-ranking="2" href="https://tabelog.com/aichi/A2301/A230110/23050032/">からみそラーメン ふくろう 本店</a>
        print(urls)

        #点数
        ratings = WebScraping.get_texts_in_class(soup, 'c-rating__val c-rating__val--strong list-rst__rating-val')
        #<span class="c-rating__val c-rating__val--strong list-rst__rating-val">3.76</span>
        print(ratings)

        return

    def test3(self):
        url = 'https://tabelog.com/aichi/A2301/A230112/23055953/'

        #soup object
        soup = WebScraping.get_soup_obj(url)

        #near_station
        near_station = WebScraping.get_texts_in_class2(soup, 'rdheader-subinfo__item rdheader-subinfo__item--station', 'linktree__parent-target-text')
        print(near_station)

        return

    def test4(self):
        url = 'https://tabelog.com/aichi/A2301/A230112/23055953/dtlrvwlst/?PG=2'

        #soup object
        soup = WebScraping.get_soup_obj(url)

        #user_name
        user_name = WebScraping.get_text_in_property(soup, property_name='v:reviewer')
        print(user_name)

        #rating
        rating = WebScraping.get_texts_in_class2(soup, 'rvw-item__ratings', 'c-rating__val c-rating__val--strong', all=False)
        print(rating)


        return



