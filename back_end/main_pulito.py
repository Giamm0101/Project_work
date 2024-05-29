import csv
from funzioni_DB import *
from Creazione_tabelle import *
from tqdm import tqdm

#Creazione database

DB_NAME = 'Ristoranti'
connection = create_server_connection('localhost', 'root', '')
execute_query(connection, f'drop database {DB_NAME}')
create_database(connection, DB_NAME)
connection2 = create_db_connection('localhost', 'root', '', DB_NAME)

# Creazione tabelle
execute_query(connection2, create_table_restaurant)
execute_query(connection2, create_table_location)
execute_query(connection2, create_table_sd)
execute_query(connection2, create_table_risto_diet)
execute_query(connection2, create_table_cuisine)
execute_query(connection2, create_table_risto_cuisine)
execute_query(connection2, create_table_users)
execute_query(connection2, create_table_review)
execute_query(connection2, alter_table_restaurant)

#Inserimento dati tipi di cucina e diete speciali

def insert_special_diets_and_cuisines(connection, lettore):
    lista_special_diet = set()
    lista_cuisine = set()

    for riga in tqdm(lettore):
        c = riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine = riga[13].split(',')
        for elem in cuisine:
            if elem:
                lista_cuisine.add(elem.strip())

    for special_diet in lista_special_diet:
        q = 'INSERT INTO special_diet(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name'
        t = (special_diet,)
        execute_query_place(connection, q, t)

    for cuisines in lista_cuisine:
        q = 'INSERT INTO cuisine(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name'
        t = (cuisines,)
        execute_query_place(connection, q, t)

#Inserimento dati location e ristoranti

def insert_data(connection, lettore):
    id = 1
    for riga in tqdm(lettore):
        q = 'INSERT INTO location(location_id, country, region, province, city) VALUES (%s, %s, %s, %s, %s)'
        t = (
            id,
            riga[3].strip() or None,
            riga[4].strip() or None,
            riga[5].strip() or None,
            riga[6].strip() or None
        )
        execute_query_place(connection, q, t)

        q = ('INSERT INTO restaurant(restaurant_link, name, awards, top_tags, price_range, '
             'features, original_open_hours, avg_rating, total_reviews_count, address, longitude, '
             'latitude, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        t = (
            riga[1].strip(), riga[2].strip(), riga[10].strip(), riga[11].strip(),
            riga[12].strip(), riga[15].strip(), riga[17].strip(), riga[18].strip(),
            riga[19].strip(), riga[7].strip(), riga[9].strip(), riga[8].strip(), id
        )
        execute_query_place(connection, q, t)
        id += 1