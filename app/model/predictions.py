import json
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt


from model import model_performance


def plot_predictions(name):
    
    predictions = model_performance(name)

    data = [
        go.Scatter(
            x=predictions.index,
            y=predictions['ARIMA Predictions'],
            mode='lines+markers'
        ),
        go.Scatter(
            x=predictions.index,
            y=predictions['Actual'],
            mode='lines+markers',
            line=dict(
                color='#f1c40f',
                dash='dash',
                width=4
            )  
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Prediction Graph for {}'.format(name),
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