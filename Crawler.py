# %%
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from re import findall
import requests
from urllib.parse import urljoin

# %%
class color:
   BOLD = '\033[1m'
   END = '\033[0m'

# %%
class SaveHouse:
    
    # id, region, town, city, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, lat, lon, last_crawled_at
    def __init__(self):
        self.houses_to_index = []
        
    def save(self, **house):
        self.houses_to_index.append(house)
        
        # if len(self.houses_to_index) == 100:
        #     helpers.bulk(es, generator(self.houses_to_index, "house-test"))
        #     print("indexed 100 houses")
        #     self.houses_to_index = []
    
    def __str__(self):
        return f'{len(self.houses_to_index)} {self.houses_to_index[-1]["id"]} {self.houses_to_index[-1]["town"]}'

# %%
class Crawler:

    def __init__(self, city_url=None):
        self.city_url = city_url
        
        self.towns_to_visit = []
        self.visited_towns = []
        
        self.houses_to_visit = []
        self.visited_houses = []
        
        self.collect_all = False
        self.save_house = SaveHouse()
        # self.page_range = [1, 2]
        
        
    def get_transform_house_data(self, urls):
        town_url = urls[0]
        house_url = urls[1]
        html = requests.get(house_url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        extract_price = lambda tag: int(tag.text.strip().split(" ")[0].replace(",", "")[:-6])

        prices_tags = soup.find_all('span', class_="color-black font-xlarge")
        price = extract_price(prices_tags[0]) if prices_tags else None
        price_per_meter = extract_price(prices_tags[1]) if prices_tags else None
        
        
        extract_number = lambda tag: [int(num) for num in tag.text.strip().split(" ") if num.isnumeric()][0]
        
        info = soup.find_all('div', class_="search-list-info")
        area = extract_number(info[0]) if info else None
        room_count = extract_number(info[1]) if info else None
        oldness = extract_number(info[2]) if info else None
        floor_count = extract_number(info[3]) if info else None
        
        
        extract_bool = lambda tag: tag.i['class'][-1].endswith("green")
        
        features = soup.find_all('span', class_="search-feature-item")
        has_parking = extract_bool(features[0]) if features else None
        has_storeroom = extract_bool(features[1]) if features else None
        has_elevator = extract_bool(features[2]) if features else None
        has_loan = extract_bool(features[3]) if features else None
        
        region = int(town_url.split("-")[2]) if town_url else None
        town = findall(r"\d-(.*)", town_url)[0]
        city = self.city_url.split("/")[-1] if self.city_url else None
        
        lat = float(findall(r"lat = (.*);", html)[0])
        lon = float(findall(r"lon = (.*);", html)[0])
        
        id_ = house_url.split("/")[-1]
        
        
        
        self.save_house.save(
            id = id_,
            region = region,
            town = town,
            city = city,
            price = price,
            price_per_meter= price_per_meter,
            area = area,
            room_count = room_count,
            oldness = oldness,
            floor_count = floor_count,
            has_parking = has_parking,
            has_storeroom = has_storeroom,
            has_elevator = has_elevator,
            has_loan = has_loan,
            lat= lat,
            lon = lon,
            last_crawled_at = datetime.now(timezone.utc).astimezone().isoformat()
        )
        print(self.save_house)
        
            
    def add_house_to_visit(self, house_url, town_url=None):
        if town_url and (town_url, house_url) not in self.visited_houses:
            # print(url)
            self.houses_to_visit.append((town_url, house_url))
            
    def get_house_url(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        for div_tag in soup.find_all('div', class_="search-results-info-boxes"):
            path = div_tag.a.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)

            self.add_house_to_visit(path, url)
        
        self.visited_towns.append(url)
    
    
    def add_town_to_visit(self, url):
        if url not in self.visited_towns:
            # print(url)
            self.towns_to_visit.append(url)
            
            
    def select_town(self, url, town_name):
        select = False
        while not select:
            select_inp = input(f"Do you want to collect {color.BOLD}{town_name}{color.END}'s apartments data? (Y/N) ")
            if select_inp.lower() == 'n':
                return False
            select = True if select_inp.lower() == 'y' else False
        
        return True
    
    
    def get_towns_url(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        for a_tag in soup.find_all('a'):
            path = a_tag.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
                
            a_tag_text = a_tag.text.strip()
            town_name = path.split("/")[-1]
            
            if a_tag_text.startswith("خرید آپارتمان") and (self.collect_all or self.select_town(path, town_name)):
                self.add_town_to_visit(path)


    def run(self):
        if self.city_url:
            collect_all_inp = input(f"Do you want to collect all towns' apartments data? (Y/N) ")
            self.collect_all = collect_all_inp.lower() == 'y'
            
            # page_range_inp = input(f"Enter page range (e.g. 1-10): ")
            # self.page_range = [int(num) for num in page_range_inp.split("-")]
            
            regions_tail = []
            for i in range(1,9):
                regions_tail.append(f"region-{i}")

            for i in range(9,22,2):
                regions_tail.append(f"region-{i}-{i+1}")
                
            regions_urls = [urljoin(self.city_url, f"/tehran/about/{tail}") for tail in regions_tail]
            print(regions_urls)
            
            while(regions_urls):
                self.get_towns_url(regions_urls.pop(0))
            
            print(self.towns_to_visit)
            with ThreadPoolExecutor(max_workers=10) as pool:
                pool.map(self.get_house_url, self.towns_to_visit)
                
            
            print(self.houses_to_visit)
            with ThreadPoolExecutor(max_workers=10) as pool:
                pool.map(self.get_transform_house_data, self.houses_to_visit)

# %%
# if __name__ == '__main__':
# c = Crawler(city_url='https://delta.ir/tehran')
# c.get_transform_house_data(("https://delta.ir/tehran/buy-apartment/region-2-saadat-abad", "https://delta.ir/tehran/buy/detail/WY3hSMOgdEk="))
Crawler(
        city_url='https://delta.ir/tehran').run()
        



