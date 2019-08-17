#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 10:03:46
# @Author  : xiedong
# @File    : weibo_spider.py

import csv
import re
import time

import requests, json
from requests.exceptions import RequestException
from pyquery import PyQuery as pq


def get_one_page(id, page):
    headers = {}
    params = {
        'containerid': '{0}_-_WEIBO_SECOND_PROFILE_WEIBO'.format(id),
        'page': page,
    }
    url = 'https://m.weibo.cn/api/container/getIndex?'
    # 通过params函数将URL补全
    response = requests.get(url, params=params, headers=headers)
    try:
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        return '索引页错误'


def parse_one_page(html):
    items = html.get('data').get('cards')
    for i in items:
        i = dict(i).get('mblog')
        # 有的是没有内容的所以需要判断是否为字典类型
        if isinstance(i, dict):
            yield {
                'id': i.get('id'),
                'text': pq(i.get('text')).text(),  # 通过pyquery将HTML标签去除
                'attitudes_count': i.get('attitudes_count'),
                'comments_count': i.get('comments_count'),
                'reposts_count': i.get('reposts_count')
            }


def main():
    user_id = {'朱一龙': '2304131594052081',
               '迪丽热巴': '2304131669879400',
               '邓伦': '2304131865901305'
               }
    name = input('Weibo_ID: ')
    id = user_id.get(name)
    current_time = time.strftime("%m%d%H%M%S", time.localtime())

    with open('{0}_{1}.csv'.format(name, current_time), 'w', encoding='GBK', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'reposts_count', 'comments_count', 'attitudes_count'])
    # 只爬取10页的内容
    for sum in range(1, 11):

        page = sum
        html = get_one_page(id, page)
        i = parse_one_page(html)

        with open('{0}_{1}.csv'.format(name, current_time), 'a', encoding='GBK', errors='ignore') as f:
            writer = csv.writer(f)
            data = list()

            for k in i:
                line = (k.get('text'), k.get('reposts_count'), k.get('comments_count'), k.get('attitudes_count'))
                data.append(line)

            writer.writerows(data)


if __name__ == '__main__':
    main()

"""
朱一龙：2304131594052081
迪丽热巴：2304131669879400
邓伦：2304131865901305
"""
"""
https://m.weibo.cn/api/container/getIndex?uid=&luicode=&lfid=&type=uid&value=&containerid=
json.data.cards.11.scheme
"""
