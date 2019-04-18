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

def graph_topo():
    import datetime
    import plotly
    import plotly.graph_objs as go
    import igraph

    node_names = ['tora', 'torb', 'torc', 'tord', 'tors', 'ctl1', 'ctl2', 'ctl3', 'stor1', 'stor2', 'stor3', 'vts1', 'vts2', 'comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'mgm']
    edge_names = ['mgm tora P1', 'mgm torb P1',
                  'tors tora P20-e1/1', 'tors torb P22-e1/2',
                  'tors torc P20-e1/1', 'tors tord P22-e1/2',
                  'ctl1 tora P2', 'ctl1 torb P2',
                  'ctl2 tora P3', 'ctl2 torb P3',
                  'ctl3 torc P1', 'ctl3 tord P1',
                  'stor1 tora P5', 'stor1 torb P5',
                  'stor2 tora P6', 'stor2 torb P6',
                  'stor3 tora P7', 'stor3 torb P7',
                  'vts1 tora po22', 'vts1 torb po22',
                  'vts2 tora po23', 'vts2 torb po23',
                  'comp1 tora po11', 'comp1 torb po11',
                  'comp2 tora po12', 'comp2 torb po12',
                  'comp3 tora po13', 'comp3 torb po13',
                  'comp4 torc po8', 'comp4 tord po8',
                  'comp5 torc po9', 'comp5 tord po9',
                  ]
    edge_ports = [x.split()[-1] for x in edge_names]
    node_colors = []
    node_labels = []
    for name in node_names:
        if 'tor' in name:
            color = 'black'
        elif 'ctl' in name:
            color = 'red'
        elif 'stor' in name:
            color = 'yellow'
        elif 'vts' in name:
            color = 'brown'
        elif 'comp' in name:
            color = 'green'
        elif 'mgm' in name:
            color = 'blue'
        else:
            color = 'magenta'
        node_colors.append(color)
        node_labels.append(f'<a href="http://lenta.ru">{name}</a>')

    gr = igraph.Graph(directed=False)
    gr.add_vertices(node_names)
    for edge_name in edge_names:
        n1, n2, port = edge_name.split()
        gr.add_edges([(n1, n2)])
    lay = gr.layout_sugiyama()

    Xn = [x[0] for x in lay]
    Yn = [x[1] for x in lay]

    n1 = go.Scatter(x=Xn, y=Yn, mode='markers+text', name='nodes', marker={'symbol': 'square', 'size': 20, 'color': node_colors}, text=node_labels, textposition='middle left', hoverinfo='none')
    Xe = []
    Ye = []
    Xc = []
    Yc = []
    Xt = []
    Yt = []
    for e in gr.es:
        x1, y1 = lay[e.source][0], lay[e.source][1]
        x2, y2 = lay[e.target][0], lay[e.target][1]
        Xe += [x1, x2, None]  # x-coordinates of edge ends
        Ye += [y1, y2, None]
        Xc.append(0.4 * x1 + 0.6 * x2)
        Yc.append(0.4 * y1 + 0.6 * y2)
        Xt.append(0.48 * x1 + 0.52 * x2)
        Yt.append(0.48 * y1 + 0.52 * y2)
    e1 = go.Scatter(x=Xe, y=Ye, mode='lines', line={'color': 'gray', 'width': 1}, hoverinfo='none')
    e2 = go.Scatter(x=Xc, y=Yc, mode='markers', text=edge_names, hoverinfo='text')
    e3 = go.Scatter(x=Xt, y=Yt, mode='text', text=edge_ports, hoverinfo='none')
    no_axis = {'showline': False, 'zeroline': False, 'showgrid': False, 'showticklabels': False, 'title': ''}
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    layout = go.Layout(title=f'topo created {now}', showlegend=False, xaxis=no_axis, yaxis=no_axis, hovermode='closest')
    plotly.offline.plot({'data': [n1, e1, e2, e3], 'layout': layout}, filename='topo_example.html', auto_open=True)


if __name__ == '__main__':
    #plot_topology()
    graph_topo()
