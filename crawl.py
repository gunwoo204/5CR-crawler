import re
import json
import random
import time

import requests
from bs4 import BeautifulSoup

from abc import ABC, abstractmethod

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
}


def remove_elements(origin: list, word: str):
    while True:
        try:
            origin.remove(word)
        except:
            break


class Company(ABC):
    def set_resp(self, url, is_enc_UTF8=True):
        time.sleep(random.random()/2)
        self.page_text = ''
        self.resp = requests.get(url, headers=HEADERS)
        if not is_enc_UTF8:
            self.resp.encoding = 'UTF-8'
        self.soup = BeautifulSoup(self.resp.text, 'lxml')

    @abstractmethod
    def crawl(self, url):
        pass

    def __init__(self) -> None:
        super().__init__()


# 보수
class Chosun(Company):  # 조선일보
    def crawl(self, url):
        self.set_resp(url)
        raw_page_text = self.soup.find('script', id='fusion-metadata').text

        semicolon_indexs = result = [_.start() for _ in re.finditer(';', raw_page_text)]  # 세미콜론 위치(index) 모두 가져옴
        quote_indexs = result = [_.start() for _ in re.finditer('"', raw_page_text)]

        for i in range(0, int(len(quote_indexs)/2)):
            for j in semicolon_indexs:
                if quote_indexs[2 * i] < j < quote_indexs[2 * i + 1]:
                    semicolon_indexs.remove(j)

        global_content = raw_page_text[semicolon_indexs[3]:semicolon_indexs[4]].replace(';Fusion.globalContent=', '')  # semicolon 4~5번째 사이의 내용을 가져와서 변수명 삭제
        content = json.loads(global_content)  # 그럼 json으로 만들 수 있음

        article_contents = content['content_elements']  # 기사 본문

        pure_articles = []
        for block in article_contents:
            if 'content' not in block:  # 이미지 block은 content가 없음
                continue
            pure_articles.append(block['content'])

        self.page_text = '\n'.join(pure_articles).replace('<br/>', '').replace('\n', ' ')


class Joongang(Company):    # 중앙일보
    def crawl(self, url):
        self.set_resp(url)

        raw_page_text = self.soup.find('div', id='article_body')
        raw_article = raw_page_text.find_all('p')
        
        for line_element in raw_article:
            self.page_text += f'{line_element.text[3:]} '


class Donga(Company): # 동아일보
    def crawl(self, url):
        self.set_resp(url)

        raw_page_text = self.soup.find('div', 'article_txt').findChildren(string=True)
        remove_elements(raw_page_text, '\n')
        remove_elements(raw_page_text, ' ')
        
        for line_element in raw_page_text:
            if line_element[0] == '#':
                break
            else:
                self.page_text += line_element


#진보
class Hankyoreh(Company): # 한겨레
    def crawl(self, url):
        self.set_resp(url)

        raw_page_text = self.soup.find('div', 'text').text.split('\n')
        remove_elements(raw_page_text, '')

        for line_element in raw_page_text[1:]:
            self.page_text += line_element


class Kyunghyang(Company):    # 경향신문
    def crawl(self, url):
        self.set_resp(url)

        raw_page_text = self.soup.find_all('p', 'content_text')

        for line_element in raw_page_text:
            self.page_text += line_element.text.split('\n')[1]


class Vop(Company):   # 민중의 소리
    def crawl(self, url):
        full_url = f'http://vop.co.kr{url}'
        self.set_resp(full_url, False)
        self.page_text = self.soup.find('div', 'editor').text.replace('\n', '')


#중도
class Seoul(Company): # 서울신문
    def crawl(self, url):
        self.set_resp(url, False)
        self.page_text = remove_elements(self.soup.find('div', id='atic_txt1').text.split('\n'), '')[0]


class Hankook(Company):   # 한국일보
    def crawl(self, url):
        self.set_resp(url)
        raw_page_text = self.soup.find_all('p', 'editor-p')
        for text in raw_page_text:
            self.page_text += text.text
