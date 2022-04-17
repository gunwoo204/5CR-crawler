from tqdm import tqdm
import pandas as pd
import crawl


def select_crawler(company: str):
    if company == 'chosun':
        return crawl.Chosun()
    elif company == 'joongang':
        return crawl.Joongang()
    elif company == 'donga':
        return crawl.Donga()
    elif company == 'hankyoreh':
        return crawl.Hankyoreh()
    elif company == 'kyunghyang':
        return crawl.Kyunghyang()
    elif company == 'vop':
        return crawl.Vop()
    elif company == 'seoul':
        return crawl.Seoul()
    elif company == 'hankook':
        return crawl.Hankook()
    else:
        return '''
        !!!ERROR!!!\tCompany name does not exist
        \tChoose one from the below
        \t[chosun joongang donga hankyoreh kyunghyang vop seoul hankook]
        '''


if __name__ == '__main__':
    company = input('[chosun joongang donga hankyoreh kyunghyang vop seoul hankook]\nselect company: ')
    crawler = select_crawler(company)

    if type(crawler) == str:
        print(crawler)
        
    else:
        opinion_list = pd.read_csv(f'data/{company}-opinion.csv')
        urls = opinion_list['URL']

        f = open(f'data/{company}-text.txt', 'w', encoding='UTF-8')
        # n = len(urls)
        n = 20
        success_counter = 0

        for url in tqdm(urls[0:n], desc='CRAWLING PROGRESS'):
            try:
                crawler.crawl(url)
                f.write(crawler.page_text)
                f.write('\n')
                success_counter += 1
            except:
                f.write('\n')
        
        print('\n----------CRAWLING END----------')
        print(f'# of articles ATTEMPTED to crawl: {n}')
        print(f'# of articles SUCCEEDED to crawl: {success_counter}\n')
        f.close()
