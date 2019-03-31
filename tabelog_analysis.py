from web_scraping import WebScraping as ws
import pandas as pd
import numpy as np
import time
import os
import codecs

class TabelogAnalysis:
    def __init__(self):
        self.WAIT_TIME = 1.5
        self.DEBUG = False
        if self.DEBUG:
            self.debug_pages = 3
            print('in Debug mode')

        return

    def ratings_csv_in_Nagoya_Ramen(self):
        print(' Rating of Nagoya Ramen Restaurant')
        #url
        #https://tabelog.com/aichi/A2301/rstLst/ramen/1/?Srt=D&SrtT=rt&sort_mode=1&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3&svd=190317&svt=1900&svps=2&select_sort_flg=1
        #url=url_p1 + index + url_p2 + url_p3 + url_p4
        url_p1 = 'https://tabelog.com/aichi/A2301/rstLst/ramen/'
        url_p2 = '/?Srt=D&SrtT=rt&sort_mode=1&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3&svd='
        url_p3 = '190324'
        url_p4 = '&svt=1900&svps=2&select_sort_flg=1'
        
        ######################
        # get restaurant info
        ######################
        # get name, tabelog_rank, url, tabelog_rating
        print('  get restaurant info')
        rst_names = []
        rst_tabelog_ranks = []
        rst_urls = []
        rst_tabelog_ratings = []
        #
        complete_restaurant_info_flag = False
        page_counter = 1
        while not complete_restaurant_info_flag:
            #set page url
            page_url = url_p1 + str(page_counter) + url_p2 + url_p3 + url_p4
            
            #soup object
            time.sleep(self.WAIT_TIME)
            soup = ws.get_soup_obj(page_url)

            #check complete
            check = ws.get_texts_in_class(soup, 'list-rst__rst-name-target')
            if check == []:
                complete_restaurant_info_flag = True
                print(' complete getting restaurant info')
            else:
                print('   page ' + str(page_counter))

                #restaurant name
                rst_names.extend(ws.get_texts_in_class(soup, 'list-rst__rst-name-target'))
                #<a class="list-rst__rst-name-target cpy-rst-name js-ranking-num" target="_blank" data-list-dest="item_top" data-ranking="2" href="https://tabelog.com/aichi/A2301/A230110/23050032/">からみそラーメン ふくろう 本店</a>

                #rank
                rst_tabelog_ranks.extend(ws.get_texts_in_class(soup, 'list-rst__rank-no'))
            
                #URL
                rst_urls.extend(ws.get_href_in_class(soup, 'list-rst__rst-name-target'))
                #<a class="list-rst__rst-name-target cpy-rst-name js-ranking-num" target="_blank" data-list-dest="item_top" data-ranking="2" href="https://tabelog.com/aichi/A2301/A230110/23050032/">からみそラーメン ふくろう 本店</a>

                #点数
                tbrt = ws.get_texts_in_class(soup, 'c-rating__val c-rating__val--strong list-rst__rating-val')
                if tbrt == []:
                    tbrt = [''] * len(check) # no rating
                rst_tabelog_ratings.extend(tbrt)
                #<span class="c-rating__val c-rating__val--strong list-rst__rating-val">3.76</span>

                page_counter += 1

            if self.DEBUG:
                if page_counter == self.debug_pages:
                    print('in debug mode')
                    break

        # get nearest station
        print('  get restaurant info (nearest station)')
        rst_near_stations = []
        for rst_url in rst_urls:
            print('   ' + rst_url)
            #soup object
            time.sleep(self.WAIT_TIME)
            soup = ws.get_soup_obj(rst_url)

            #near_station
            ns = ws.get_texts_in_class2(soup, 'rdheader-subinfo__item rdheader-subinfo__item--station', 'linktree__parent-target-text')
            if ns == []:
                ns = ws.get_texts_in_class(soup, 'rdheader-subinfo__item-text')[0]
                ns = ws.delete_brank_linefeed_in_str(str(ns))
                ns = [ns]

            #near_station
            #rst_near_stations.extend(ws.get_texts_in_class2(soup, 'rdheader-subinfo__item rdheader-subinfo__item--station', 'linktree__parent-target-text'))
            rst_near_stations.extend(ns)
            

        ######################
        # get user ratings
        ######################
        print('  get user ratings')
        rating_rst_name = []
        rating_user_names = []
        ratings = []
        # per restaurant
        for i, rst_url in enumerate(rst_urls):
            print('   ' + rst_url)
            #
            page_counter = 1
            complete_flag = False
            while not complete_flag:
                # page url
                page_url = rst_url + 'dtlrvwlst/?PG=' + str(page_counter)

                #soup object
                time.sleep(self.WAIT_TIME)
                soup = ws.get_soup_obj(page_url)

                #check complete
                check = ws.get_text_in_property(soup, property_name='v:reviewer')
                if check == []:
                    complete_flag = True
                else:
                    print('    page ' + str(page_counter))
                    #rating_rst_name
                    rating_rst_name.extend([rst_names[i]]*len(check))
                    
                    #user_name
                    rating_user_names.extend(ws.get_text_in_property(soup, property_name='v:reviewer'))

                    #rating
                    ratings.extend(ws.get_texts_in_class2(soup, 'rvw-item__ratings', 'c-rating__val c-rating__val--strong', all=False))

                    page_counter += 1

                if self.DEBUG:
                    if page_counter == self.debug_pages:
                        print('in debug mode')
                        break
            
        ######################
        # summary
        ######################
        print('summary')
        print(' rst_names : {0}'.format(len(rst_names)))
        print(' rst_tabelog_ranks : {0}'.format(len(rst_tabelog_ranks)))
        print(' rst_urls : {0}'.format(len(rst_urls)))
        print(' rst_tabelog_ratings : {0}'.format(len(rst_tabelog_ratings)))
        rating_num = 0
        for rating in ratings:
            rating_num += len(rating)
        print(' all rating num : {0}'.format(rating_num))

        # save
        oup_dir = ws.make_output_dir()
        self.save_data(oup_dir, rst_names, rst_tabelog_ranks, rst_tabelog_ratings, rst_near_stations, rst_urls, rating_rst_name, rating_user_names, ratings)

        return

    def save_data(self, output_dir, rst_names, rst_tabelog_ranks, rst_tabelog_ratings, rst_near_stations, rst_urls, rating_rst_names, rating_user_names, ratings):
        ######################
        # save
        ######################
        # restaurant info
        #  name, tabelog_rank, tabelog_rating, url
        rst_info = pd.concat([pd.DataFrame(rst_names), 
                              pd.DataFrame(rst_tabelog_ranks), 
                              pd.DataFrame(rst_tabelog_ratings), 
                              pd.DataFrame(rst_near_stations),
                              pd.DataFrame(rst_urls)], 
                             axis=1)
        rst_info.columns = ['restaurant_name', 'tabelog_rank', 'tabelog_rating', 'nearest_station', 'url']
        filename = os.path.join(output_dir, 'restaurant_info.csv')
        with codecs.open(filename, 'w', 'shift_jis', 'replace') as f:
            rst_info.to_csv(f, index=False)

        # rating
        #  restaurant_name, user_name, rating
        rating_summary = pd.concat([pd.DataFrame(rating_rst_names), 
                                    pd.DataFrame(rating_user_names), 
                                    pd.DataFrame(ratings)], 
                                   axis=1)
        rating_summary.columns = ['restaurant_name', 'user_name', 'rating']
        filename = os.path.join(output_dir, 'rating.csv')
        with codecs.open(filename, 'w', 'shift_jis', 'replace') as f:
            rating_summary.to_csv(f, index=False)

        return


tbl = TabelogAnalysis()
tbl.ratings_csv_in_Nagoya_Ramen()