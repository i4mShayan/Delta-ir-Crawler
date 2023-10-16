from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Crawler:

    def __init__(self, city_url=None):
        self.city_url = city_url
        
        self.towns_to_visit = []
        self.visited_towns = []
        
        self.houses_to_visit = []
        self.visited_houses = []
        
        self.house_count = 0
            
        
    # def get_houses_url(self, url, html):
    #     soup = BeautifulSoup(html, 'html.parser')
    #     for content in soup.find_all('div', class_="search-results-info-boxes"):
    #         path = content.a.get('href')
    #         if path and path.startswith('/'):
    #             path = urljoin(url, path)
    #         yield path      
    
    def add_towns_to_visit(self, url):
        if url not in self.visited_towns and url not in self.towns_to_visit:
            print(url)
            self.towns_to_visit.append(url)
            
    def select_town(self, url, town_name):
        select = False
        while not select:
            select_inp = input(f"Do you want to collect {color.BOLD}{town_name}{color.END}'s apartments data? (Y/N) ")
            if select_inp.lower() == 'n':
                return False
            select = True if select_inp.lower() == 'y' else False
        
        return True
    
    def get_towns_url(self, url, html, collect_all=True):
        soup = BeautifulSoup(html, 'html.parser')
        for a_tag in soup.find_all('a'):
            path = a_tag.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
                
            a_tag_text = a_tag.string.strip()
            town_name = path.split("/")[-1]
            
            if a_tag_text.startswith("خرید") and (collect_all or self.select_town(path, town_name)):
                yield path
    
    def crawl_towns(self, url):
        html = requests.get(url).text
        
        collect_all_inp = input(f"Do you want to collect all towns' apartments data? (Y/N) ")
        collect_all = True if collect_all_inp.lower() == 'y' else False
        page_range_inp = input(f"Enter page range (e.g. 1-10): ")
        page_range = list(int(num)for num in page_range_inp.split("-"))
        
        for url in self.get_towns_url(url, html, collect_all=collect_all):
               self.add_towns_to_visit(url)

    # def crawl(self, url):
    #     html = requests.get(url).text
    #     for url in self.get_houses_url(url, html):
    #         self.add_url_to_visit(url)

    def run(self):
        if self.city_url:
            self.crawl_towns(self.city_url)
            
        
        
        # while self.urls_to_visit:
        #     url = self.urls_to_visit.pop(0)
        #     print("Crawling: ", url, " ...")
        #     try:
        #         self.crawl(url)
        #     except Exception:
        #         pass
        #         # logging.exception(f'Failed to crawl: {url}')
        #     finally:
        #         self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(
        city_url='https://delta.ir/newcity/getlocationurlseodepositlinks?locationId=33').run()