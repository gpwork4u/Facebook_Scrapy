import scrapy
from facebook_scrapy.items import PostItem
from facebook_scrapy.settings import EMAIL, PASSWORD
import pickle
import requests
import logging
import os
import time
from bs4 import BeautifulSoup
import json

USER_ID = 'user id'
def save_cookies(session, filename):
    with open(filename, 'wb') as f:
        pickle.dump(session.cookies, f)


def load_cookies(filename):
    with open(filename, 'rb') as f:
        return dict(pickle.load(f))


class facebook(scrapy.Spider):
    name = "facebook"
    headers = {
        'scheme': 'https',
        'accept': '*/*',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) ' +
        'Gecko/20100101 Firefox/76.0',
    }

    def login(self, email, password):
        # get input field
        session = requests.session()
        session.cookies.clear()
        if os.path.isfile(email+'.cookie'):
            return load_cookies(email+'.cookie')
        url = 'https://mbasic.facebook.com/login'
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        all_input_data = soup.find('form').findAll(
            'input', {'type': 'hidden'})
        data = {}
        for input_data in all_input_data:
            data[input_data.get('name')] = input_data.get('value')
        # input email and password
        data['email'] = email
        data['pass'] = password
        # login
        login_url = 'https://mbasic.facebook.com/login'
        req = session.post(login_url, data=data, headers=self.headers)
        # get hidden input data
        url = 'https://mbasic.facebook.com/'
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        try:
            self.fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        except Exception as e:
            logging.debug(e)
            logging.error('username or password is invalid')
            return False
        save_cookies(session, email+'.cookie')
        return load_cookies(email+'.cookie')

    def start_requests(self):
        cookies = self.login(EMAIL, PASSWORD)
        url = 'https://mbasic.facebook.com/profile/timeline/stream/?' + \
            'end_time=%s&' % str(time.time()) + \
            'profile_id=%s' % str(USER_ID)
        urls = [
            url,
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        item = PostItem()
        article_section = response.css('section')
        articles = article_section.xpath('article')
        for article in articles:
            if 'data-ft' not in article.attrib:
                continue
            data = json.loads(article.attrib['data-ft'])
            item['author'] = data['mf_story_key']
            item['author'] = article.css('strong').css('a::text').get()
            item['content'] = ''
            for p in article.css('span').css('p'):
                for a in p.css('a::text').getall():
                    item['content'] += a + ' '
                if len(p.css('p::text').get()) > 0:
                    item['content'] += p.css('p::text').get() + '\n'
            item['images'] = []
            for img in article.css('img'):
                item['images'].append(img.attrib['src'])
            item['post_url'] = 'https://mbasic.facebook.com/story.php?story_fbid=%s&id=1' % item['author']
            item['time'] = article.css('abbr::text').get()
            yield item