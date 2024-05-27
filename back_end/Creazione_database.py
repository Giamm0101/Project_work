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
execute_query(connection2, create_table_country)
execute_query(connection2, create_table_region)
execute_query(connection2, create_table_province)
execute_query(connection2, create_table_city)
execute_query(connection2, create_table_sd)
execute_query(connection2, create_table_risto_diet)
execute_query(connection2, create_table_cuisine)
execute_query(connection2, create_table_risto_cuisine)
execute_query(connection2, create_table_users)
execute_query(connection2, create_table_review)


with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    lettore= csv.reader(file, delimiter= ",")
    next(lettore)
    lista_special_diet = set()
    lista_cuisine = set()
    lista_country = set()
    lista_region = set()
    for riga in lettore:
        c= riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine= riga[13].split(',')
        for elem in cuisine:
            if elem != '':
                lista_cuisine.add(elem.strip())
        lista_country.add(riga[3].strip())
        if riga[4]!= '':
            lista_region.add(riga[4].strip())
    lista_special_diet= list(lista_special_diet)
    lista_country= list(lista_country)
    lista_region= list(lista_region)



for special_diet in lista_special_diet:
    q= ('INSERT INTO special_diet(name) VALUES(%s)')
    t = (special_diet, )
    execute_query_place(connection2, q, t)

for cuisines in lista_cuisine:
    q= ('INSERT INTO cuisine(name) VALUES(%s)')
    t = (cuisines, )
    execute_query_place(connection2, q, t)

for country in lista_country:
    q= ('INSERT INTO country(name) VALUES(%s)')
    t = (country, )
    execute_query_place(connection2, q, t)

for region in lista_region:
    r= 'SELECT country_id FROM country WHERE country_id=%s'
    q= ('INSERT INTO region(name, country_id) VALUES(%s, %s)')
    t = (region, r)
    execute_query_place(connection2, q, t)



