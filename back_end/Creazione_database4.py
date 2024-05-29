import csv
from funzioni_DB import *
from Creazione_tabelle import *
from tqdm import tqdm

DB_NAME = 'Ristoranti'
MAX_ROWS = 1000

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

def fetch_query_results(connection, query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result

def insert_special_diets_and_cuisines(connection, lettore):
    lista_special_diet = set()
    lista_cuisine = set()
    row_count = 0

    for riga in tqdm(lettore):
        if row_count >= MAX_ROWS:
            break
        c = riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine = riga[13].split(',')
        for elem in cuisine:
            if elem:
                lista_cuisine.add(elem.strip())
        row_count += 1

    for special_diet in lista_special_diet:
        q = 'INSERT INTO special_diet(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name'
        t = (special_diet,)
        execute_query_place(connection, q, t)

    for cuisines in lista_cuisine:
        q = 'INSERT INTO cuisine(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name'
        t = (cuisines,)
        execute_query_place(connection, q, t)

def insert_data(connection, lettore):
    id = 1
    row_count = 0

    for riga in tqdm(lettore):
        if row_count >= MAX_ROWS:
            break
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
        row_count += 1

def insert_associations(connection, lettore):
    row_count = 0

    for riga in tqdm(lettore):
        if row_count >= MAX_ROWS:
            break
        restaurant_link = riga[1].strip()
        special_diet_list = [diet.strip() for diet in riga[14].split(',') if diet.strip()]

        for elem in special_diet_list:
            restaurant_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_link = %s"
            restaurant_id = fetch_query_results(connection, restaurant_query, (restaurant_link,))
            diet_query = "SELECT special_diet_id FROM special_diet WHERE name = %s"
            diet_id = fetch_query_results(connection, diet_query, (elem,))

            if restaurant_id and diet_id:
                link_query = "INSERT INTO risto_diet (restaurant_id, special_diet_id) VALUES (%s, %s)"
                execute_query_place(connection, link_query, (restaurant_id[0][0], diet_id[0][0]))
        row_count += 1

# First pass to insert special diets and cuisines
with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_special_diets_and_cuisines(connection2, lettore)

# Second pass to insert location and restaurant data
with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_data(connection2, lettore)

# Third pass to insert associations
with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_associations(connection2, lettore)

