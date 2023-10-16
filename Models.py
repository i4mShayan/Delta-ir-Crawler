class House:
    def __init__(self, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city):
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

    @classmethod
    def create(cls, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city):
        house = cls(price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city)
        town.house_list.append(house)
        city.towns[town.name].house_list.append(house)
        return house


class Town:
    def __init__(self, name, city, house_list):
        self.name = name
        self.city = city
        self.house_list = house_list

    @classmethod
    def create(cls, name, city):
        town = cls(name, city, [])
        city.towns[name] = town
        return town


class City:
    def __init__(self, name, towns):
        self.name = name
        self.towns = towns

    @classmethod
    def create(cls, name):
        city = cls(name, {})
        return city

