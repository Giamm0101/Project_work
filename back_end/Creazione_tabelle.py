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
    location_id INT,
    address VARCHAR(150),
    longitude FLOAT,
    latitude FLOAT
);
"""

create_table_location = """
CREATE TABLE location (
location_id INT PRIMARY KEY,
country VARCHAR(100),
region VARCHAR(150),
province VARCHAR(150),
city VARCHAR(150)
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
restaurant_link INT,
title VARCHAR(150),
data VARCHAR(150),
target VARCHAR(100),
t_review VARCHAR(700),
punteggio VARCHAR(50),
photo1 VARCHAR(200),
photo2 VARCHAR(200),
PRIMARY KEY (restaurant_link, users_id),
FOREIGN KEY (restaurant_link) REFERENCES restaurant(restaurant_link),
FOREIGN KEY (users_id) REFERENCES users(users_id)
);
"""

alter_table_restaurant = """
ALTER TABLE restaurant
ADD FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE RESTRICT;
"""


