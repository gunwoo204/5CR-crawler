from time import sleep
import pandas as pd
import crawl


if __name__ == '__main__':
    newspaper = 'chosun'
    opinion_list = pd.read_csv(f'data/{newspaper}-opinion.csv')
    f = open(f'data/{newspaper}-text.txt', 'w', encoding='UTF-8')

    urls = opinion_list['URL']

    chosun_crawler = crawl.Chosun()
    i = 0
    for url in urls[0:100]:
        print(f'{i} {url}')
        crawl_data = chosun_crawler.crawl(url)
        f.write(crawl_data)
        f.write('\n')
        i += 1
    f.close()
