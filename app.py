from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
@app.route('/')  # route di default con slash
def home():
    return render_template("home.html")

@app.route('/ristoranti')
def ristoranti():
    return render_template("ristoranti.html")

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