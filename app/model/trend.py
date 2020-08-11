import json
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose 

from processing import readFile


new_data, date = readFile()

def plot_trend(name):
    a = seasonal_decompose(new_data[name], model = "add")
#     plot = a.seasonal.plot();
#     print(a.seasonal.values)
    
    data = [
        go.Scatter(
            x=date,
            y=a.trend.values,
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Trend Graph for {}'.format(name),
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