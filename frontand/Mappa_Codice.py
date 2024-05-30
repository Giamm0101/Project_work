import mysql.connector
import folium
from folium.plugins import MarkerCluster
import logging
from tqdm import tqdm

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG)

logging.debug('Inizio del programma')

try:
    # Connessione al database
    logging.debug('Tentativo di connessione al database')
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ristoranti"
    )
    logging.debug('Connessione al database riuscita')

    cursor = conn.cursor()
    logging.debug('Esecuzione della query per recuperare i dati')
    cursor.execute("SELECT name, top_tags, latitude, longitude FROM restaurant")
    ristoranti = cursor.fetchall()
    logging.debug(f'Recupero dei dati completato: {len(ristoranti)} ristoranti trovati')

    # Chiudi la connessione al database
    cursor.close()
    conn.close()
    logging.debug('Connessione al database chiusa')

    # Definisci i limiti della mappa
    lat_min, lon_min = 34.0, -10.0
    lat_max, lon_max = 72.0, 40.0

    # Crea una mappa centrata in Europa con limiti
    logging.debug('Creazione della mappa centrata in Europa')
    mappa = folium.Map(
        location=[54.5260, 15.2551],
        zoom_start=4,
        max_bounds=True
    )
    mappa.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])

    # Aggiungi i ristoranti alla mappa con clustering
    logging.debug('Aggiunta dei ristoranti alla mappa con clustering')
    marker_cluster = MarkerCluster().add_to(mappa)
    for nome, top_tags, lat, lon in tqdm(ristoranti, desc="Aggiunta dei ristoranti alla mappa"):
        if lat == 0 or lon == 0:
            logging.debug(f'Salto del ristorante {nome} per coordinate non valide ({lat}, {lon})')
            continue
        logging.debug(f'Aggiunta del ristorante: {nome} con coordinate ({lat}, {lon})')
        folium.Marker(location=[lat, lon], popup=(nome, top_tags)).add_to(marker_cluster)

    # Salva la mappa come file HTML
    logging.debug('Salvataggio della mappa come file HTML')
    mappa.save('mappa_ristoranti.html')
    logging.debug('Mappa salvata come file HTML con successo')

except mysql.connector.Error as err:
    logging.error(f'Errore durante la connessione al database: {err}')
except Exception as e:
    logging.error(f'Errore generale: {e}')

logging.debug('Fine del programma')
