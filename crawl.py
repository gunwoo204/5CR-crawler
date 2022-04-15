import re
import json

import requests
from bs4 import BeautifulSoup

from abc import ABC, abstractmethod

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
}


class Company(ABC):
    def set_resp(self, url, is_enc_UTF8=False):
        self.resp = requests.get(url, headers=HEADERS)
        self.soup = BeautifulSoup(self.resp.text, 'lxml')
        if is_enc_UTF8:
            self.resp.encoding = 'UTF-8'

    @abstractmethod
    def crawl(self, url):
        pass


# 보수
class Chosun(Company):
    def crawl(self, url):
        self.set_resp(url, True)
        page_text = self.soup.find('script', id='fusion-metadata').text

        semicolon_indexs = result = [_.start() for _ in re.finditer(';', page_text)]  # 세미콜론 위치(index) 모두 가져옴
        quote_indexs = result = [_.start() for _ in re.finditer('"', page_text)]

        for i in range(0, int(len(quote_indexs)/2)):
            for j in semicolon_indexs:
                if quote_indexs[2 * i] < j < quote_indexs[2 * i + 1]:
                    semicolon_indexs.remove(j)

        global_content = page_text[semicolon_indexs[3]:semicolon_indexs[4]].replace(';Fusion.globalContent=', '')  # semicolon 4~5번째 사이의 내용을 가져와서 변수명 삭제
        content = json.loads(global_content)  # 그럼 json으로 만들 수 있음

        article_contents = content['content_elements']  # 기사 본문

        pure_articles = []
        for block in article_contents:
            if 'content' not in block:  # 이미지 block은 content가 없음
                continue
            pure_articles.append(block['content'])

        return '\n'.join(pure_articles).replace('<br/>', '').replace('\n', ' ')


class Joongang(Company):
    def crawl(self, url):
        self.set_resp(url)

        page_text = self.soup.find('div', id='article_body')
        raw_article = page_text.find_all('p')
        article_text = ''

        for article_part in raw_article:
            article_text += f'{article_part.text[3:]} '

        return article_text


def donga(url: str) -> str: # 동아일보
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', 'article_txt').findChildren(string=True)
    while True:
        try:
            page_text.remove('\n')
        except:
            try:
                page_text.remove(' ')
            except:
                break
    
    article_text = ''
    for text in page_text:
        if text[0] == '#':
            break
        else:
            article_text += text
            
    return article_text


#진보
def hankyoreh(url: str) -> str: # 한겨레
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', 'text').text.split('\n')
    while True:
        try:
            page_text.remove('')
        except:
            break

    article_text = ''
    for text in page_text[1:]:
        article_text += text
    return article_text


def kyunghyang(url: str) -> str:    # 경향신문
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find_all('p', 'content_text')

    article_text = ''
    for text in page_text:
        raw_text = text.text.split('\n')
        article_text += raw_text[1]
    return article_text


def vop(url: str) -> str:   # 민중의 소리
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', 'editor').text

    return page_text


#중도
def seoul(url: str) -> str: # 서울신문
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', id='atic_txt1').text.split('\n')

    while True:
        try:
            page_text.remove('')
        except:
            break
    
    return page_text[1]


def hankook(url: str) -> str:   # 한국일보
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find_all('p', 'editor-p')

    article_text = ''

    for text in page_text:
        article_text += text.text

    return article_text


def financial(url: str) -> str: # 파이낸셜뉴스
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', id='article_content').text.split('\n')

    while True:
        try:
            page_text.remove('')
        except:
            break

    article_text = ''
    for text in page_text[4:-2]:
        article_text += text

    return article_text