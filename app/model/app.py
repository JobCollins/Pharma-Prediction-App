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
    bar = None
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['medicinal drug']

            bar = plot_product(name)
        else:
            flash('Error: All Fields are Required')

    return render_template('app.html', form=form, plot=bar)


def plot_product(name):

    new_data, date = readFile()

    # plt.figure(figsize=(16,4))
    
    # plt.plot(date, new_data[name])
    # plt.xlabel('Time')
    # plt.ylabel('Sale')
    # plt.title(f'Sales for {name}')
    # plt.show() 

    data = [
        go.Scatter(
            x=date,
            y=new_data[name],
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Historical Trend Graph',
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

    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph


if __name__ == "__main__":
    app.run(port=3000, debug=True)