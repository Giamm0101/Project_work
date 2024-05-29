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

def execute_batch_query(connection, query, params_list):
    try:
        cursor = connection.cursor()
        cursor.executemany(query, params_list)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def insert_special_diets_and_cuisines(connection, lettore):
    lista_special_diet = set()
    lista_cuisine = set()

    for riga in tqdm(lettore[:MAX_ROWS]):  # Limit to MAX_ROWS
        c = riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine = riga[13].split(',')
        for elem in cuisine:
            if elem:
                lista_cuisine.add(elem.strip())

    special_diet_queries = [('INSERT INTO special_diet(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name', (sd,)) for sd in lista_special_diet]
    cuisine_queries = [('INSERT INTO cuisine(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name', (c,)) for c in lista_cuisine]

    for q, t in special_diet_queries + cuisine_queries:
        execute_query_place(connection, q, t)

def insert_data(connection, lettore):
    location_queries = []
    restaurant_queries = []

    id = 1
    for riga in tqdm(lettore[:MAX_ROWS]):  # Limit to MAX_ROWS
        location_queries.append((
            id,
            riga[3].strip() or None,
            riga[4].strip() or None,
            riga[5].strip() or None,
            riga[6].strip() or None
        ))

        restaurant_queries.append((
            riga[1].strip(), riga[2].strip(), riga[10].strip(), riga[11].strip(), riga[12].strip(),
            riga[15].strip(), riga[17].strip(), riga[18].strip(), riga[19].strip(), riga[7].strip(),
            riga[9].strip(), riga[8].strip(), id
        ))

        id += 1

    execute_batch_query(connection,
        'INSERT INTO location(location_id, country, region, province, city) VALUES (%s, %s, %s, %s, %s)',
        location_queries)
    execute_batch_query(connection,
        ('INSERT INTO restaurant(restaurant_link, name, awards, top_tags, price_range, features, '
         'original_open_hours, avg_rating, total_reviews_count, address, longitude, latitude, location_id) '
         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
        restaurant_queries)

def insert_associations(connection, data, query_template, fetch_query, param_index):
    association_queries = []
    restaurant_cache = {}
    item_cache = {}

    limited_data = data[:MAX_ROWS]  # Limit to MAX_ROWS

    # Caching all restaurants
    for riga in tqdm(limited_data, desc='Caching Restaurants'):
        restaurant_link = riga[1].strip()
        if restaurant_link not in restaurant_cache:
            restaurant_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_link = %s"
            restaurant_cache[restaurant_link] = fetch_query_results(connection, restaurant_query, (restaurant_link,))

    # Caching all items (special diets or cuisines)
    for riga in tqdm(limited_data, desc='Caching Items'):
        association_list = [elem.strip() for elem in riga[param_index].split(',') if elem.strip()]
        for elem in association_list:
            if elem not in item_cache:
                item_cache[elem] = fetch_query_results(connection, fetch_query, (elem,))

    # Creating association queries
    for riga in tqdm(limited_data, desc='Creating Associations'):
        restaurant_link = riga[1].strip()
        restaurant_id = restaurant_cache.get(restaurant_link)[0][0] if restaurant_cache.get(restaurant_link) else None

        association_list = [elem.strip() for elem in riga[param_index].split(',') if elem.strip()]
        for elem in association_list:
            item_id = item_cache.get(elem)[0][0] if item_cache.get(elem) else None
            if restaurant_id and item_id:
                association_queries.append((restaurant_id, item_id))

    execute_batch_query(connection, query_template, association_queries)

# Read CSV data into a list
with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = list(csv.reader(file, delimiter=","))
    lettore.pop(0)  # Remove header line

# Primo passaggio per inserire diete speciali e cucine
insert_special_diets_and_cuisines(connection2, lettore)

# Secondo passaggio per inserire dati di location e ristoranti
insert_data(connection2, lettore)

# Terzo passaggio per inserire associazioni (diete)
insert_associations(connection2, lettore,
                    "INSERT INTO risto_diet (restaurant_id, special_diet_id) VALUES (%s, %s)",
                    "SELECT special_diet_id FROM special_diet WHERE name = %s", 14)

# Terzo passaggio per inserire associazioni (cucine)
insert_associations(connection2, lettore,
                    "INSERT INTO risto_cuisine (restaurant_id, cuisine_id) VALUES (%s, %s)",
                    "SELECT cuisine_id FROM cuisine WHERE name = %s", 13)
