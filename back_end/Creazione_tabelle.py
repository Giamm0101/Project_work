create_table_restaurant = """
CREATE TABLE restaurant (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_link VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    awards VARCHAR(500), 
    top_tags VARCHAR(250),
    price_range VARCHAR(100),
    features VARCHAR(500),
    original_open_hours VARCHAR(500),
    avg_rating FLOAT,
    total_reviews_count INT,
    city_id INT UNIQUE,
    address VARCHAR(150),
    longitude FLOAT,
    latitude FLOAT
);
"""

create_table_country = """
CREATE TABLE country (
country_id INT PRIMARY KEY,
name VARCHAR(100)
);
"""

create_table_region = """
CREATE TABLE region (
region_id INT PRIMARY KEY,
name VARCHAR(100),
country_id INT,
FOREIGN KEY (country_id) REFERENCES country(country_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);
"""

create_table_province = """
CREATE TABLE province (
province_id INT PRIMARY KEY,
name VARCHAR(100),
region_id INT,
FOREIGN KEY (region_id) REFERENCES region(region_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);
"""


create_table_city = """
CREATE TABLE city (
city_id INT PRIMARY KEY,
name VARCHAR(100),
province_id INT,
FOREIGN KEY (province_id) REFERENCES province(province_id)
ON DELETE CASCADE
ON UPDATE CASCADE
);
"""

create_table_sd = """
CREATE TABLE special_diet (
special_diet_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100)
);
"""

create_table_risto_diet = """
CREATE TABLE risto_diet (
restaurant_id INT,
special_diet_id INT,
PRIMARY KEY (restaurant_id, special_diet_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
FOREIGN KEY (special_diet_id) REFERENCES special_diet(special_diet_id)
);
"""

create_table_cuisine = """
CREATE TABLE cuisine (
cuisine_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100)
);
"""

create_table_risto_cuisine = """
CREATE TABLE risto_cuisine (
restaurant_id INT,
cuisine_id INT,
PRIMARY KEY (restaurant_id, cuisine_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
FOREIGN KEY (cuisine_id) REFERENCES cuisine(cuisine_id)
);
"""

create_table_users = """
CREATE TABLE users (
users_id INT AUTO_INCREMENT PRIMARY KEY,
nickname VARCHAR(150) NOT NULL,
name VARCHAR(150) NOT NULL,
surname VARCHAR(150) NOT NULL,
email VARCHAR(150) NOT NULL,
password VARCHAR(15) NOT NULL
);
"""

create_table_review = """
CREATE TABLE review (
users_id INT,
restaurant_id INT,
PRIMARY KEY (restaurant_id, users_id),
FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
FOREIGN KEY (users_id) REFERENCES users(users_id)
);
"""

alter_table_restaurant = """
ALTER TABLE restaurant
ADD FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE RESTRICT
);
"""
