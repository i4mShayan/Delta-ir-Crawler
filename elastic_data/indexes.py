from elasticsearch import Elasticsearch

# Create an Elasticsearch client
es = Elasticsearch()

# Index names
city_index = "cities"
town_index = "towns"
house_index = "houses"

def index_house(house):
    # Convert the House object to a dictionary
    house_dict = {
        "price": house.price,
        "price_per_meter": house.price_per_meter,
        "area": house.area,
        "room_count": house.room_count,
        "oldness": house.oldness,
        "floor_count": house.floor_count,
        "has_parking": house.has_parking,
        "has_storeroom": house.has_storeroom,
        "has_elevator": house.has_elevator,
        "has_loan": house.has_loan,
        "town": house.town.name,
        "city": house.city.name,
        "web_link": house.web_link
    }

    # Index the house document in Elasticsearch
    es.index(index=house_index, body=house_dict)

def index_town(town):
    # Convert the Town object to a dictionary
    town_dict = {
        "name": town.name,
        "city": town.city.name
    }

    # Index the town document in Elasticsearch
    es.index(index=town_index, body=town_dict)

def index_city(city):
    # Convert the City object to a dictionary
    city_dict = {
        "name": city.name
    }

    # Index the city document in Elasticsearch
    es.index(index=city_index, body=city_dict)