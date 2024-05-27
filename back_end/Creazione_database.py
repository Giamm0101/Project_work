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
    lista_country = []
    lista_region = []
    lista_province= []
    lista_city = []
    for riga in lettore:
        c= riga[14].split(',')
        for elem in c:
            lista_special_diet.add(elem.strip())
        cuisine= riga[13].split(',')
        for elem in cuisine:
            if elem != '':
                lista_cuisine.add(elem.strip())
        lista_country.append(riga[3].strip())
        lista_region.append(riga[4].strip())
        lista_province.append(riga[5].strip())
        lista_city.append(riga[6])
    lista_special_diet= list(lista_special_diet)
    set_country= set(lista_country)
    set_region= set(lista_region)
    set_province= set(lista_province)
    set_city= set(lista_city)

diz_country= {}
id= 1
for country in set_country:
    if country not in diz_country:
        diz_country[country]= id
        id+=1


diz_region={}
id_region = 1
for country, region in zip(lista_country, lista_region):
    diz_region[region] = {'id_region' : id_region, 'country': diz_country[country]}
    id_region+=1

diz_province={}
id_province=1
for region, province in zip(lista_region, lista_province):
    diz_province[province] = {'id_province': id_province, 'region' : diz_region[region]['id_region']}
    id_province+=1
diz_city={}
id_city=1
for province, city in zip(lista_province, lista_city):
    diz_city[city] = {'id_city' : id_city, 'province' : diz_province[province]['id_province']}
    id_city +=1


for k,v in diz_country.items():
    q= ('INSERT INTO country(name, country_id) VALUES(%s,%s)')
    t = (k, v)
    execute_query_place(connection2, q, t)
for k in diz_region:
    q = ('INSERT INTO region(region_id, name, country_id) VALUES(%s, %s, %s)')
    region_id = diz_region[k]['id_region']
    country_id = diz_region[k]['country']
    t= (region_id,k, country_id)
    execute_query_place(connection2, q, t)
for k in diz_province:
    q = ('INSERT INTO province(province_id, name, region_id) VALUES(%s, %s, %s)')
    province_id = diz_province[k]['id_province']
    region_id = diz_province[k]['region']
    t= (province_id,k, region_id)
    execute_query_place(connection2, q, t)
for k in diz_city:
    q = ('INSERT INTO city(city_id, name, province_id) VALUES(%s, %s, %s)')
    city_id = diz_city[k]['id_city']
    province_id = diz_city[k]['province']
    t= (city_id,k, province_id)
    execute_query_place(connection2, q, t)


for special_diet in lista_special_diet:
    q= ('INSERT INTO special_diet(name) VALUES(%s)')
    t = (special_diet, )
    execute_query_place(connection2, q, t)

for cuisines in lista_cuisine:
    q= ('INSERT INTO cuisine(name) VALUES(%s)')
    t = (cuisines, )
    execute_query_place(connection2, q, t)

print(diz_city)









