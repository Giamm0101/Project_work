from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.config.from_object('config.Config')

def create_db_connection():
    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    return mysql.connector.connect(**db_config)

def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

@app.route('/')  # route di default con slash
def home():
    return render_template("home.html")

@app.route('/ristoranti', methods=['GET', 'POST'])
def ristoranti():
    if request.method == 'POST':

        city = request.form['city']
        diet = request.args.get('diet')

        # Conta il numero totale di ristoranti
        query = """SELECT COUNT(*) as n FROM restaurant AS r JOIN risto_diet AS rd ON r.restaurant_id=rd.restaurant_id JOIN special_diet as sp 
        ON rd.special_diet_id=sp.special_diet_id JOIN location AS l ON r.location_id=l.location_id WHERE l.city = %s"""
        params = [city]
        if diet:
            query += " AND rd.special_diet_id = %s"
            params.append(diet)

        nr = execute_query(query, tuple(params))
        nr = nr[0]['n']
        
        # Gestione della paginazione
        np = request.args.get('page')
        if np is None:
            np = 0
        else:
            np = int(np)
        
        # Recupera i ristoranti per la pagina corrente
        query = """SELECT * FROM restaurant AS r JOIN risto_diet AS rd ON r.restaurant_id=rd.restaurant_id JOIN special_diet as sp 
        ON rd.special_diet_id=sp.special_diet_id JOIN location AS l ON r.location_id=l.location_id WHERE l.city = %s GROUP BY r.restaurant_id"""
        if diet:
            query += " AND rd.special_diet_id = %s"
        query += " LIMIT 15 OFFSET %s"
        params.append(np * 15)
        
        ristoranti = execute_query(query, tuple(params))
        print(ristoranti[0])
        
        return render_template("ristoranti.html", ristoranti=ristoranti, page=np, max_page=(nr // 15))
    else:
        # Handle the initial GET request (no city provided)
        city = None  # Or set a default city
        ristoranti = []  # Empty list of restaurants
        page = 0
        max_page = 0  # Set appropriate values for pagination
        return render_template("ristoranti.html", ristoranti=ristoranti, page=page, max_page=max_page)


@app.route('/ristoranti/<country>')
def ristoranti_country(country):
    nr = execute_query('SELECT COUNT(*) as n FROM restaurant AS r JOIN location AS l ON r.location_id = l.location_id WHERE l.country = %s ', (country,))
    nr = nr[0]['n']
    np =request.args.get('page')
    if np == None:
        np =0
    else:
        np = int(np)
    ristoranti = execute_query('SELECT * FROM restaurant AS r JOIN location AS l ON r.location_id = l.location_id WHERE l.country = %s LIMIT 15 offset %s', (country,np*15) )
    return render_template("ristoranti_country.html", ristoranti=ristoranti, page = np, max_page = nr//15, country = country)
    #return ristoranti

@app.route('/chi_siamo')
def chi_siamo():
    return render_template('chi_siamo.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

@app.route('/mappa')
def mappa():
    return render_template('mappa.html')


if __name__ == '__main__':
    app.run(debug=True)