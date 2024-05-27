from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)
app.config.from_object('config.Config')


@app.route('/')
def home():

    return render_template('home.html', titolo=''.upper())
    