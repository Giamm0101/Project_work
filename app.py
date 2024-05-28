from flask import Flask, render_template


app = Flask(__name__)
@app.route('/')  # route di default con slash
def home():
    return render_template("home.html")

@app.route('/chi_siamo')
def chi_siamo():
    return render_template('chi_siamo_html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

if __name__ == '__main__':
    app.run(debug=True)