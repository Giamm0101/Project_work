import pandas as pd
from faker import Faker

# Inizializza il generatore di dati finti
fake = Faker()

# Numero di record da generare
num_records = 2701  # Puoi cambiare questo valore come desideri

# Liste per salvare i dati
data = {
    'Nickname': [],
    'Nome': [],
    'Cognome': [],
    'Email': [],
    'Password': []
}

# Genera dati randomici
for _ in range(num_records):
    data['Nickname'].append(fake.user_name())
    data['Nome'].append(fake.first_name())
    data['Cognome'].append(fake.last_name())
    data['Email'].append(fake.email())
    data['Password'].append(fake.password())

# Crea un DataFrame con i dati
df = pd.DataFrame(data)

# Salva il DataFrame in un file CSV
df.to_csv('users.csv', index=False)

print(f"Generato file CSV con {num_records} record.")