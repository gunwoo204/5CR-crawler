import re
import json

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
}


# 보수
def chosun(url: str) -> str:    # 조선일보
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('script', id='fusion-metadata').text

    semicolon_indexs = result = [_.start() for _ in re.finditer(';', page_text)]  # 세미콜론 위치(index) 모두 가져옴
    global_content = page_text[semicolon_indexs[3]:semicolon_indexs[4]].replace(';Fusion.globalContent=', '')  # semicolon 4~5번째 사이의 내용을 가져와서 변수명 삭제
    content = json.loads(global_content)  # 그럼 json으로 만들 수 있음

    article_contents = content['content_elements']  # 기사 본문

    pure_articles = []
    for block in article_contents:
        if 'content' not in block:  # 이미지 block은 content가 없음
            continue
        pure_articles.append(block['content'])

    return '\n'.join(pure_articles)


def joongang(url: str) -> str:  # 중앙일보
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'lxml')

    page_text = soup.find('div', id='article_body')
    raw_article = page_text.find_all('p')
    article_text = ''

    for article_part in raw_article:
        article_text += f'{article_part.text[3:]} '
        
    return article_text


def donga(url: str) -> str: # 동아일보
    pass


#진보
def hankyoreh(url: str) -> str: # 한겨레
    pass


def kyunghyang(url: str) -> str:    # 경향신문
    pass


def vop(url: str) -> str:   # 민중의 소리
    pass


#중도
def seoul(url: str) -> str: # 서울신문
    pass


def hankook(url: str) -> str:   # 한국일보
    pass


def naeil(url: str) -> str: # 내일신문
    pass