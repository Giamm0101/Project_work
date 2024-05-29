import csv
import math

from funzioni_DB import *
from Creazione_tabelle import *
from tqdm import tqdm

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


def fetch_query_results(connection, query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result


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
        execute_query_place2(connection, q, t)
    connection.commit()

    for cuisines in lista_cuisine:
        q = 'INSERT INTO cuisine(name) VALUES(%s) ON DUPLICATE KEY UPDATE name = name'
        t = (cuisines,)
        execute_query_place2(connection, q, t)
    connection.commit()


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


def insert_data_location(connection, lettore):
    id = 1
    q = 'INSERT INTO location(location_id, country, region, province, city) VALUES (%s, %s, %s, %s, %s)'
    tt = []
    for riga in tqdm(lettore):
        t = (
            id,
            riga[3].strip() or None,
            riga[4].strip() or None,
            riga[5].strip() or None,
            riga[6].strip() or None
        )
        tt.append(t)
        id += 1

    s = 20
    part_size = math.ceil(len(tt) / s)

    # Dividi tt in cinque parti ed esegui l'inserimento per ciascuna parte
    for i in range(s):
        part = tt[i * part_size:(i + 1) * part_size]
        if part:  # Assicurati che la parte non sia vuota
            execute_query_place_many(connection, q, None, part)


def insert_data_restaurant(connection, lettore):
    id = 1
    q = ('INSERT INTO restaurant(restaurant_link, name, awards, top_tags, price_range, '
         'features, original_open_hours, avg_rating, total_reviews_count, address, longitude, '
         'latitude, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    tt = []

    diz_ris = {}
    for riga in tqdm(lettore):
        t = (
            riga[1].strip(), riga[2].strip(), riga[10].strip(), riga[11].strip(),
            riga[12].strip(), riga[15].strip(), riga[17].strip(), riga[18].strip(),
            riga[19].strip(), riga[7].strip(), riga[9].strip(), riga[8].strip(), id
        )
        tt.append(t)

        diz_ris[riga[1].strip()] = id

        id += 1

    s = 150
    part_size = math.ceil(len(tt) / s)

    # Dividi tt in cinque parti ed esegui l'inserimento per ciascuna parte
    for i in range(s):
        part = tt[i * part_size:(i + 1) * part_size]
        if part:  # Assicurati che la parte non sia vuota
            execute_query_place_many(connection, q, None, part)

    return diz_ris


#Inserimento associazioni ristorante diete speciali
def insert_associations(connection, lettore, diz_ris):
    diz = {}
    link_query = "INSERT INTO risto_diet (restaurant_id, special_diet_id) VALUES (%s, %s)"
    lista_dati = []
    for riga in tqdm(lettore):
        restaurant_link = riga[1].strip()
        special_diet_list = [diet.strip() for diet in riga[14].split(',') if diet.strip()]
        # print(special_diet_list)
        restaurant_id = diz_ris[restaurant_link]
        # print(restaurant_id)

        for elem in special_diet_list:
            # restaurant_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_link = %s"
            # restaurant_id = fetch_query_results(connection, restaurant_query, (restaurant_link,))
            if elem not in diz:
                diet_query = "SELECT special_diet_id FROM special_diet WHERE name = %s"
                diet_id = fetch_query_results(connection, diet_query, (elem,))
                diz[elem] = diet_id[0][0]

            lista_dati.append((restaurant_id, diz[elem]))

    # for elem in special_diet_list:
    #     restaurant_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_link = %s"
    #     restaurant_id = fetch_query_results(connection, restaurant_query, (restaurant_link,))
    #     diet_query = "SELECT special_diet_id FROM special_diet WHERE name = %s"
    #     diet_id = fetch_query_results(connection, diet_query, (elem,))
    #     # if elem not in diz:
    #     #     diet_query = "SELECT special_diet_id FROM special_diet WHERE name = %s"
    #     #     diet_id = fetch_query_results(connection, diet_query, (elem,))
    #     #     diz[elem] = diet_id[0][0]
    #
    #     lista_dati.append((restaurant_id, diet_id))

    s = 150
    part_size = math.ceil(len(lista_dati) / s)

    # Dividi tt in cinque parti ed esegui l'inserimento per ciascuna parte
    for i in range(s):
        part = lista_dati[i * part_size:(i + 1) * part_size]
        if part:  # Assicurati che la parte non sia vuota
            execute_query_place_many(connection, link_query, None, part)


    #Inserimento associazioni ristorante cucine
def insert_associations_cuisine(connection, lettore, diz_ris):
    diz = {}
    link_query = "INSERT INTO risto_cuisine (restaurant_id, cuisine_id) VALUES (%s, %s)"
    lista_dati_cuisine = []
    for riga in tqdm(lettore):
        restaurant_link = riga[1].strip()
        cuisine_list = [cuisine.strip() for cuisine in riga[13].split(',') if cuisine.strip()]

        restaurant_id = diz_ris[restaurant_link]


        for elem in cuisine_list:
            # restaurant_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_link = %s"
            # restaurant_id = fetch_query_results(connection, restaurant_query, (restaurant_link,))
            if elem not in diz:
                cuisine_query = "SELECT cuisine_id FROM cuisine WHERE name = %s"
                cuisine_id = fetch_query_results(connection, cuisine_query, (elem,))
                diz[elem] = cuisine_id[0][0]

            lista_dati_cuisine.append((restaurant_id, diz[elem]))

    s = 150
    part_size = math.ceil(len(lista_dati_cuisine) / s)

    # Dividi tt in cinque parti ed esegui l'inserimento per ciascuna parte
    for i in range(s):
        part = lista_dati_cuisine[i * part_size:(i + 1) * part_size]
        if part:  # Assicurati che la parte non sia vuota
            execute_query_place_many(connection, link_query, None, part)


def insert_associations_reviews(connection, lettore, diz_ris):
    link_query = ('INSERT INTO review(users_id, restaurant_id, restaurant_link, title, review_date, target, t_review, punteggio, photo1, photo2)'
            ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
    for riga in tqdm(lettore):
        user_id = riga[8]
        title = riga[0]
        restaurant_link = riga[1]
        data = riga[2]
        target = riga[3]
        t_review = riga[4]
        punteggio = riga[5]
        photo1 = riga[6]
        photo2 = riga[7]

        restaurant_id = diz_ris[restaurant_link]
        t = (user_id, restaurant_id,restaurant_link, title, data, target, t_review, punteggio, photo1, photo2)
        execute_query_place(connection, link_query, t)


# First pass to insert special diets and cuisines
with open('back_end/Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_special_diets_and_cuisines(connection2, lettore)

# Second pass to insert location and restaurant data
with open('back_end/Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_data_location(connection2, lettore)

with open('back_end/Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    diz_ris = insert_data_restaurant(connection2, lettore)
#
# # Third pass to insert associations
with open('back_end/Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_associations(connection2, lettore, diz_ris)

#Inserimento cucine
with open('back_end/Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_associations_cuisine(connection2, lettore, diz_ris)


with open('users_definitivo.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    for riga in lettore:
        q= 'INSERT INTO users(nickname, name, surname, email, password) VALUES (%s,%s,%s,%s,%s)'
        nick= riga[0]
        name=riga[1]
        surname=riga[2]
        email=riga[3]
        password=riga[4]
        t=(nick, name, surname, email, password)
        execute_query_place(connection2, q, t)

with open('recensioni_totali_user.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    insert_associations_reviews(connection2, lettore, diz_ris)
    #i ristoranti recensiti sono solo 181 in totale
