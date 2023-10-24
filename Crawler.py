import requests
import json
import multiprocessing as mp
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class color:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class SaveHouse:
    # price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city
    def __init__(self, **kwargs):
        self.data = kwargs

    def run(self):
        es.index(index='test', doc_type='_doc', body=data)



class Crawler:

    def __init__(self, city_url=None):
        self.city_url = city_url
        
        self.towns_to_visit = set()
        self.visited_towns = list()
        
        self.houses_to_visit = set()
        self.visited_houses = list()
        
        self.house_count = 0
        # self.page_range = [1, 2]
        
    def get_house_data(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        prices_tags = soup.find_all('span', _class="color-black font-xlarge")
        price = prices_tags[0].string.strip() if prices_tags else None
        price_per_meter = prices_tags[1].string.strip() if prices_tags else None
        
        info = soup.find_all('div', _class="search-list-info")
        area = info[0].string.strip() if info else None
        room_count = info[1].string.strip() if info else None
        oldness = info[2].string.strip() if info else None
        floor_count = info[3].string.strip() if info else None
        
        s = "s"
        s.endswith()
        
        features = soup.find_all('span', _class="search-feature-item")
        has_parking = True if features[0].i['class'][0].endswith("green") else False
        has_storeroom = True if features[1].i['class'][0].endswith("green") else False
        has_elevator = True if features[2].i['class'][0].endswith("green") else False
        has_loan = True if features[3].i['class'][0].endswith("green") else False
        
        town = soup.find('h1', _class="search-list-title2").string.strip().split("،")[-1]
        city = "Tehran"
        
        SaveHouse(
            price=price,
            price_per_meter=price_per_meter,
            area=area,
            room_count=room_count,
            oldness=oldness,
            floor_count=floor_count,
            has_parking=has_parking,
            has_storeroom=has_storeroom,
            has_elevator=has_elevator,
            has_loan=has_loan,
            town=town,
            city=city
        ).run()
        
        
            
    def add_house_to_visit(self, url):
        if url not in self.visited_houses:
            print(url)
            self.houses_to_visit.add(url)
            
    def get_house_url(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        for div_tag in soup.find_all('div', _class="search-results-info-boxes"):
            path = div_tag.a.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)

            self.add_house_to_visit(path)
    
    
    def add_town_to_visit(self, url):
        if url not in self.visited_towns:
            print(url)
            self.towns_to_visit.add(url)
            
            
    def select_town(self, url, town_name):
        select = False
        while not select:
            select_inp = input(f"Do you want to collect {color.BOLD}{town_name}{color.END}'s apartments data? (Y/N) ")
            if select_inp.lower() == 'n':
                return False
            select = True if select_inp.lower() == 'y' else False
        
        return True
    
    
    def get_towns_url(self, url, collect_all=True):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        for a_tag in soup.find_all('a'):
            path = a_tag.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
                
            a_tag_text = a_tag.string.strip()
            town_name = path.split("/")[-1]
            
            if a_tag_text.startswith("خرید") and (collect_all or self.select_town(path, town_name)):
                self.add_town_to_visit(path)


    def run(self):
        if self.city_url:
            collect_all_inp = input(f"Do you want to collect all towns' apartments data? (Y/N) ")
            collect_all = True if collect_all_inp.lower() == 'y' else False
            
            # page_range_inp = input(f"Enter page range (e.g. 1-10): ")
            # self.page_range = [int(num) for num in page_range_inp.split("-")]
            
            self.get_towns_url(self.city_url, collect_all=collect_all)
            
            with mp.Pool(processes=5) as pool:
                pool.map(self.crawl_towns, self.towns_to_visit)
            with mp.Pool(processes=5) as pool:
                pool.map(self.get_house_data, self.houses_to_visit)
            
            

if __name__ == '__main__':
    c = Crawler()
    c.crawl_towns("https://delta.ir/tehran/buy-apartment/region-3-jordan")
    # Crawler(
    #     city_url='https://delta.ir/newcity/getlocationurlseodepositlinks?locationId=33').run()