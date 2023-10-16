from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        
        self.towns_to_visit = []
        self.visited_towns = []
        
        self.houses_to_visit = []
        self.visited_houses = []
        
        self.count = 0
            
    def get_info(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        # for prop in soup.find_all('div', ):
            
    
    def add_towns_to_visit(self, url):
        if url not in self.visited_towns and url not in self.towns_to_visit:
            self.towns_to_visit.append(url)
            
    def select_town(self, url, town_name):
        select = False
        while not select:
            select_inp = input(f"Do you want to collect {town_name}'s apartments data? (Y/N) ")
            if select_inp.lower() == 'n':
                return False
            select = True if select_inp.lower() == 'y' else False
        
        self.add_towns_to_visit(url)
        return True
               

    def crawl(self, url):
        html = requests.get(url).text
        for url in self.get_houses_url(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            self.count += 1
            # logging.info(f'Crawling: {url} {self.count}')
            try:
                self.crawl(url)
            except Exception:
                pass
                # logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://delta.ir/tehran/buy-apartment/region-3-jordan']).run()