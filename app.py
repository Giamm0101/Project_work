from flask import Flask, request, jsonify, render_template
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
    ristoranti = execute_query('SELECT * FROM book')
    return render_template("ristoranti.html", ristoranti=ristoranti)

@app.route('/chi_siamo')
def chi_siamo():
    return render_template('chi_siamo.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')
cards = [{'id': i, 'title': f'Card {i}', 'content': f'Content of card {i}'} for i in range(1, 101)]

# Numero di card per pagina
CARDS_PER_PAGE = 10

@app.route('/api/cards')
def get_cards():
    page = int(request.args.get('page', 1))
    start = (page - 1) * CARDS_PER_PAGE
    end = start + CARDS_PER_PAGE
    paginated_cards = cards[start:end]
    return jsonify(paginated_cards)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)