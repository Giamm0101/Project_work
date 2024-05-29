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

@app.route('/ristoranti')
def ristoranti():
    nr = execute_query('SELECT COUNT(*) as n FROM restaurant ')
    nr = nr[0]['n']
    np =request.args.get('page')
    if np == None:
        np =0
    else:
        np = int(np)
    ristoranti = execute_query('SELECT * FROM restaurant LIMIT 15 offset %s', (np*15,))
    return render_template("ristoranti.html", ristoranti=ristoranti, page = np, max_page = nr//15)

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


if __name__ == '__main__':
    app.run(debug=True)