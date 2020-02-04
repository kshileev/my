def simple():
    import math
    import plotly
    import plotly.graph_objs as go

    sec = 1
    n_per_period = 100
    period = 10 * sec
    delta = period / n_per_period
    n_periods = 4
    n_points = n_periods * n_per_period
    omega = 2 * math.pi / period
    phase = math.pi / 2 + 0.1

    times = [x * delta for x in range(n_points)]
    sin = [1.0 * math.sin(omega * x) for x in times]
    cos = [1.0 * math.cos(omega * x - phase) for x in times]


    n1 = go.Scatter(x=times, y=sin, mode='lines', name='nodes', marker={'symbol': 'square'})
    n2 = go.Scatter(x=times, y=cos, mode='lines', name='nodes', marker={'symbol': 'square'})

    a1 = go.layout.Annotation(x=0.5, y=1.0, text='Custom annotation', xref='paper', yref='paper', showarrow=False)
    layout = go.Layout(title={'text': 'some text'}, showlegend=False, xaxis={'title': 'time, sec'}, yaxis={'title': 'amplitude, km'}, annotations=[a1])

    plotly.offline.plot({'data': [n1, n2], 'layout': layout}, filename='plotly_simple.html', auto_open=True)


if __name__ == '__main__':
    simple()
