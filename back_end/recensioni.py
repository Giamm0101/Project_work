import pandas as pd
import csv
from funzioni_DB import *

# Caricare i quattro file CSV
df1 = pd.read_csv('recensioni_pulite_eng.csv')
df2 = pd.read_csv('recensioni_pulite_ita.csv')
df3 = pd.read_csv('recensioni_pulite_france.csv')
df4 = pd.read_csv('recensioni_pulite_spain.csv')


combined_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

combined_df.to_csv('combined_file.csv', index=False)


#Inserimento dati users
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
        execute_query_place(connection)


