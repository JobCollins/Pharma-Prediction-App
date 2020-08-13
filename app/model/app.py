from flask import Flask, render_template, flash, request, Response
from wtforms import Form, SelectField, validators, SubmitField

import json
import plotly
import plotly.graph_objs as go

from processing import readFile
from seasonality import plot_seasonality
from trend import plot_trend
from predictions import plot_predictions

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
    choices = list(new_data.columns)
    form = PredictionForm(request.form)
    bar = None
    season_graph = None
    trend_graph = None
    predictions = None
    if request.method == 'POST':
        name = request.form['medicine']

        bar = plot_product(name)

        season_graph = plot_seasonality(name)

        trend_graph = plot_trend(name)

        predictions = plot_predictions(name)

    return render_template('app.html', form=form, plot=bar, choices=choices, seasonality=season_graph, trend = trend_graph, predictions=predictions)


def plot_product(name):

    new_data, date = readFile()

    data = [
        go.Scatter(
            x=date,
            y=new_data[name],
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Historical Trend Graph for {}'.format(name),
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Months',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Sale Qty',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig.layout.plot_bgcolor = 'rgba(230, 236, 245, 0.1)'
    fig.layout.paper_bgcolor = 'rgba(230, 236, 245, 0.1)'

    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph


if __name__ == "__main__":
    app.run(port=3000, debug=True)