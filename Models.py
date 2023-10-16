class House:
    def __init__(self, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, hometown, city):
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
        self.hometown = hometown
        self.city = city

    @classmethod
    def create(cls, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, hometown, city):
        house = cls(price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, hometown, city)
        hometown.house_list.append(house)
        city.hometowns[hometown.name].house_list.append(house)
        return house


class Hometown:
    def __init__(self, name, city, house_list):
        self.name = name
        self.city = city
        self.house_list = house_list

    @classmethod
    def create(cls, name, city):
        hometown = cls(name, city, [])
        city.hometowns[name] = hometown
        return hometown


class City:
    def __init__(self, name, hometowns):
        self.name = name
        self.hometowns = hometowns

    @classmethod
    def create(cls, name):
        city = cls(name, {})
        return city