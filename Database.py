import mysql.connector

# Create a MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create a cursor object
cursor = connection.cursor()

# Function to save a house to the database
def save_house(house):
    query = "INSERT INTO houses (id, price, price_per_meter, area, room_count, oldness, floor_count, has_parking, has_storeroom, has_elevator, has_loan, town, city, web_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        house.id, house.price, house.price_per_meter, house.area, house.room_count, house.oldness,
        house.floor_count, house.has_parking, house.has_storeroom, house.has_elevator, house.has_loan,
        house.town.name, house.city.name, house.web_link
    )
    cursor.execute(query, values)
    connection.commit()


# Function to save a town to the database
def save_town(town):
    query = "INSERT INTO towns (id, name, city) VALUES (%s, %s, %s)"
    values = (town.id, town.name, town.city.name)
    cursor.execute(query, values)
    connection.commit()


# Function to save a city to the database
def save_city(city):
    query = "INSERT INTO cities (id, name) VALUES (%s, %s)"
    values = (city.id, city.name)
    cursor.execute(query, values)
    connection.commit()


# Function to update a house in the database
def update_house(house):
    query = "UPDATE houses SET price = %s, price_per_meter = %s, area = %s, room_count = %s, oldness = %s, floor_count = %s, has_parking = %s, has_storeroom = %s, has_elevator = %s, has_loan = %s, town = %s, city = %s, web_link = %s WHERE id = %s"
    values = (
        house.price, house.price_per_meter, house.area, house.room_count, house.oldness,
        house.floor_count, house.has_parking, house.has_storeroom, house.has_elevator, house.has_loan,
        house.town.name, house.city.name, house.web_link, house.id
    )
    cursor.execute(query, values)
    connection.commit()


# Function to update a town in the database
def update_town(town):
    query = "UPDATE towns SET name = %s, city = %s WHERE id = %s"
    values = (town.name, town.city.name, town.id)
    cursor.execute(query, values)
    connection.commit()


# Function to update a city in the database
def update_city(city):
    query = "UPDATE cities SET name = %s WHERE id = %s"
    values = (city.name, city.id)
    cursor.execute(query, values)
    connection.commit()


# Function to get a city by name from the database
def exists_city(name):
    query = "SELECT * FROM cities WHERE name = %s"
    values = (name,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result is not None