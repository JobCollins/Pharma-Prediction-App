import json
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt


from model import predictions


def plot_predictions(name):
    
    df = predictions(name)

    data = [
        go.Scatter(
            x=df.index,
            y=df['Prediction'],
            mode='lines+markers'
        ),
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