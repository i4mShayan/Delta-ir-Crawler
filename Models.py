import Database as db

class House:
    _id_counter = 1  # Class-level counter for generating incremental IDs

    def __init__(self, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city, web_link, id=None):
        self.price = price
        self.price_per_meter = price_per_meter
        self.area = area
        self.room_count = room_count
        self.oldness = oldness
        self.floor_count = floor_count
        self.has_parking = has_parking
        self.has_storeroom = has_storeroom
        self.has_elevator = has_elevator
        self.has_loan = has_loan
        self.town = town
        self.city = city
        self.web_link = web_link
        self.id = House._id_counter if id is None else id

    @classmethod
    def create(cls, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city, web_link):
        existing_town = city.towns.get(town.name)
        if existing_town:
            town_obj = existing_town
        else:
            town_obj = Town.create(town.name, city)

        house = cls(price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town_obj, city, web_link)
        town_obj.house_list.append(house)
        db.save_house(house)
        House._id_counter += 1
        return house


class Town:
    _id_counter = 1  # Class-level counter for generating incremental IDs

    def __init__(self, name, city, house_list, id=None):
        self.id = Town._id_counter
        self.name = name
        self.city = city
        self.house_list = house_list
        self.id = Town._id_counter if id is None else id

    @classmethod
    def create(cls, name, city):
        existing_town = city.towns.get(name)
        if existing_town:
            return existing_town

        town = cls(name, city, [])
        city.towns[name] = town
        db.save_town(town)
        Town._id_counter += 1
        return town


class City:
    _id_counter = 1  # Class-level counter for generating incremental IDs

    def __init__(self, name, towns, id=None):
        self.id = City._id_counter
        self.name = name
        self.towns = towns
        self.id = City._id_counter if id is None else id

    @classmethod
    def create(cls, name):
        exists_city = db.exists_city(name)
        if exists_city:
            return None  # TODO: return object of existing city

        city = cls(name, {})
        db.save_city(city)
        City._id_counter += 1
        return city