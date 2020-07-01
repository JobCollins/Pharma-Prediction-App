from flask import Flask, render_template, flash, request, Response
from wtforms import Form, SelectField, validators, SubmitField

import json
import plotly
import plotly.graph_objs as go

from processing import readFile

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

new_data, date = readFile()

products = list(new_data.columns)
products_copy = products.copy()

choices = list(zip(products, products_copy))

class PredictionForm(Form):
    name = SelectField(u'Medicinal Drug', choices=choices)

@app.route("/", methods=['GET', 'POST'])
def history():
    form = PredictionForm(request.form)

    if request.method == 'POST':
        if form.validate():
            name = request.form['medicinal drug']