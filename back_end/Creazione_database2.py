import csv
from funzioni_DB import *
from Creazione_tabelle import *

DB_NAME= 'Ristoranti'
connection = create_server_connection('localhost', 'root', '')
execute_query(connection, f'drop database {DB_NAME}')
create_database(connection, DB_NAME)
connection2= create_db_connection('localhost', 'root', '', DB_NAME)

#Creazione tabelle
execute_query(connection2, create_table_restaurant)
execute_query(connection2, create_table_location)
execute_query(connection2, create_table_sd)
execute_query(connection2, create_table_risto_diet)
execute_query(connection2, create_table_cuisine)
execute_query(connection2, create_table_risto_cuisine)
execute_query(connection2, create_table_users)
execute_query(connection2, create_table_review)
execute_query(connection2, alter_table_restaurant)


with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore= csv.reader(file, delimiter= ",")
    next(lettore)
    lista_special_diet = set()
    lista_cuisine = set()
    for riga in lettore:
        c= riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine= riga[13].split(',')
        for elem in cuisine:
            if elem != '':
                lista_cuisine.add(elem.strip())
    lista_special_diet= list(lista_special_diet)


    for special_diet in lista_special_diet:
        q= ('INSERT INTO special_diet(name) VALUES(%s)')
        t = (special_diet, )
        execute_query_place(connection2, q, t)

    for cuisines in lista_cuisine:
        q= ('INSERT INTO cuisine(name) VALUES(%s)')
        t = (cuisines, )
        execute_query_place(connection2, q, t)

with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    for riga in lettore:
        q=('INSERT INTO location(country, region, province, city) VALUES (%s, %s, %s, %s)')
        c= riga[3].strip()
        if c == '':
            c= None
        r= riga[4].strip()
        if r== '':
            r= None
        p= riga[5].strip()
        if p== '':
            p= None
        city= riga[6].strip()
        if city== '':
            city= None
        t= (c, r, p, city)
        execute_query_place(connection2, q, t)

with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore = csv.reader(file, delimiter=",")
    next(lettore)
    for riga in lettore:
        v = "SELECT location_id FROM location WHERE country = %s AND region = %s AND province = %s AND city = %s;"
        t_t = (riga[3], riga[4], riga[5], riga[6])
        location_id = read_query_place(connection2, v, t_t)
        q = ('INSERT INTO restaurant(restaurant_link, name, awards, top_tags, price_range, '
             'features, original_open_hours, avg_rating, total_reviews_count, address, longitude, latitude, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)')
        r1= riga[1].strip()
        r2 = riga[2].strip()
        r3 = riga[10].strip()
        r4 = riga[11].strip()
        r5 = riga[12].strip()
        r6 = riga[15].strip()
        r7 = riga[17].strip()
        r8 = riga[18].strip()
        r9 = riga[19].strip()
        r10 = riga[7].strip()
        r11 = riga[9].strip()
        r12 = riga[8].strip()
        t= (r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, location_id)
        execute_query_place(connection2, q, t)
















