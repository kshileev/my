def plot_topology():
    import plotly
    import plotly.graph_objs as go

    x = ['torab', 'srv1', 'srv2', 'srv3', 'torab']
    y = ['tor-', 'comp', 'comp', 'comp', 'tor+']
    names = list(range(len(x)))
    colors = list(range(len(x)))
    n1 = go.Scatter(x=x, y=y, mode='markers+text', marker={'symbol': 'square', 'size': 20, 'color': colors}, text=names, textposition='bottom right',
                    hoverinfo='none')
    annotations = [{'x': xy[0], 'y': xy[1], 'text': 'some text', 'showarrow': False, 'ay': -40 } for xy in zip(x, y)]
    no_axis = {'showline': False, 'zeroline': False, 'showgrid': False, 'showticklabels': False, 'title': ''}
    layout = go.Layout(title='Test scatter', showlegend=False, xaxis=no_axis, yaxis=no_axis, hovermode='closest', annotations=annotations)
    plotly.offline.plot({'data': [n1], 'layout': layout}, filename='plotly_scatter.html', auto_open=True)


if __name__ == '__main__':
    plot_topology()
