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


#with open('Dataset_ancora_più_pulito.csv', encoding='utf-8') as file:
    #lettore= csv.reader(file, delimiter= ",")
    #next(lettore)