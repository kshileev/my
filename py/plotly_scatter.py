def plot_topology(pod):
    import datetime
    import plotly
    import plotly.graph_objs as go
    import igraph
    import os
    import random
    import webbrowser

    # mgm node
    node_names = [pod.mgm.os_id]
    node_labels = [f'<a href="https://{pod.mgm.hard_ctl.ip}">mgm</a>']
    node_colors = ['magenta']
    # tors
    node_names += [x.os_id for x in pod.tors]
    node_labels += [f'<a href="https://{x.ip}">{x.os_id}</a>' for x in pod.tors]
    node_colors += ['black'] * len(pod.tors)
    # hosts
    node_names += [x.os_id for x in pod.hosts]
    node_labels += [f'<a href="https://{x.hard_ctl.ip}">{x.os_id}</a>' for x in pod.hosts]
    node_colors += [x.color for x in pod.hosts]

    gr = igraph.Graph(directed=False)
    gr.add_vertices(node_names)
    edge_names = []
    edge_ports = []
    for tor in pod.tors:
        for link in tor.links:
            edge_names.append(str(link))
            edge_ports.append(f'{link.po1}')
            gr.add_edges([(link.n1.os_id, link.n2.os_id)])
    lay = gr.layout_sugiyama()

    x_n = [x[0] for x in lay]
    y_n = [x[1] for x in lay]

    plot_nodes = go.Scatter(x=x_n, y=y_n, mode='markers+text', marker={'symbol': 'square', 'size': 20, 'color': node_colors}, text=node_labels, textposition='middle left', hoverinfo='none')
    edge_x = []
    edge_y = []
    link_x = []
    link_y = []
    port_x = []
    port_y = []
    for e in gr.es:
        x1, y1 = lay[e.source][0], lay[e.source][1]
        x2, y2 = lay[e.target][0], lay[e.target][1]
        edge_x += [x1, x2, None]  # x-coordinates of edge ends
        edge_y += [y1, y2, None]
        link_x.append(0.1 * x1 + 0.9 * x2)
        link_y.append(0.1 * y1 + 0.9 * y2)
        port_x.append(0.3 * x1 + 0.7 * x2)
        port_y.append(0.3 * y1 + 0.7 * y2)
    e1 = go.Scatter(x=edge_x, y=edge_y, mode='lines', line={'color': 'gray', 'width': 1}, hoverinfo='none')  # link lines
    e2 = go.Scatter(x=link_x, y=link_y, mode='markers', text=edge_names, hoverinfo='text')       # link info
    e3 = go.Scatter(x=port_x, y=port_y, mode='text', text=edge_ports, hoverinfo='none')  # po info

    annotations = [go.layout.Annotation(x=0.5, y=1.08, text=f'a {pod.nets_d["a"].vlan_id} {pod.nets_d["a"].cidr}', xref='paper', yref='paper', showarrow=False),
                   go.layout.Annotation(x=0.5, y=1.06, text=f'm {pod.nets_d["m"].vlan_id} {pod.nets_d["m"].cidr}', xref='paper', yref='paper', showarrow=False),
                   go.layout.Annotation(x=0.5, y=1.04, text=f'e {pod.nets_d["e"].vlan_id} {pod.nets_d["e"].cidr}', xref='paper', yref='paper', showarrow=False),
                   go.layout.Annotation(x=0.5, y=1.02, text=f'p {pod.nets_d["p"].vlan_id} {pod.nets_d["e"].cidr}', xref='paper', yref='paper', showarrow=False)]

    no_axis = {'showline': False, 'zeroline': False, 'showgrid': False, 'showticklabels': False, 'title': ''}
    layout = go.Layout(title=f'{pod.name}', showlegend=False, xaxis=no_axis, yaxis=no_axis, hovermode='closest', annotations=annotations)

    html_name = f'{pod.name}.{datetime.datetime.now().strftime("%d-%b-%y")}.html'
    plotly.offline.plot({'data': [plot_nodes, e1, e2, e3], 'layout': layout}, filename=html_name, auto_open=False, auto_play=False)
    os.system(f'scp {html_name} store:/var/www/topo/')
    webbrowser.open(f'http://172.29.173.233/topo/{html_name}')


class Cimc:
    def __init__(self, ip):
        self.ip = ip


class Host:
    def __init__(self, color, os_id, ip):
        self.os_id = os_id
        self.color = color
        self.hard_ctl = Cimc(ip=ip)
        self.links = []
        self.name = 'g7-2.' + self.os_id


class Tor:
    def __init__(self,os_id, ip):
        self.os_id = os_id
        self.name = 'g7-2.' + self.os_id
        self.ip = ip
        self.links = []


class Link(object):
    SRC_SETUP = 'SETUP'
    SRC_SETUP_BY_LDDP = 'SETUP_MODIFIED_BY_LLDP'
    SRC_LLDP = 'LLDP'

    def __repr__(self):
        po1 = self.po1 if '.' in self.po1 else 'po' + self.po1
        po2 = self.po2 if '.' in self.po2 else 'po' + self.po2
        return f'{self.n1.name}.{self.p1}({po1})->{self.n2.name}.{self.p2}({po2}) {self.src}'

    def __init__(self, n1, p1, po1, n2, p2, po2=None, src=SRC_SETUP):
        self.n1 = n1
        self.p1 = p1
        self.n2 = n2
        self.p2 = p2
        self.po1 = str(po1)
        self.po2 = str(po2)  # po2 is mac if it's tor -> host connection
        self.src = src  # where this link comes from: setup_data or lldp
        n1.links.append(self)
        n2.links.append(self)


class Net:
    def __init__(self, name, vlan_id, cidr):
        self.name = name
        self.vlan_id = vlan_id
        self.cidr = cidr


class Pod:
    def __init__(self):
        self.name = 'g7-2'
        self.mgm = Host(color='magenta', os_id='mgm', ip='11.11.11.11')
        self.tors = [Tor(os_id='tora', ip='10.10.10.1'), Tor(os_id='torb', ip='10.10.10.2'), Tor(os_id='torc', ip='10.10.10.3'), Tor(os_id='tord', ip='10.10.10.4'), Tor(os_id='tors', ip='10.10.10.5')]
        self.hosts = [Host(color='green', os_id='comp1', ip='1.1.1.21'), Host(color='green', os_id='comp2', ip='1.1.1.22'), Host(color='green', os_id='comp3', ip='1.1.1.23'), Host(color='green', os_id='comp4', ip='1.1.1.24'),
                      Host(color='red', os_id='ctl1', ip='1.1.1.11'), Host(color='red', os_id='ctl2', ip='1.1.1.12'), Host(color='red', os_id='ctl3', ip='1.1.1.13'),
                      Host(color='brown', os_id='stor1', ip='1.1.1.31'), Host(color='brown', os_id='stor2', ip='1.1.1.32'), Host(color='brown', os_id='stor3', ip='1.1.1.33'),
                      Host(color='yellow', os_id='vts1', ip='1.1.1.41'), Host(color='yellow', os_id='vts2', ip='1.1.1.42')]

        Link(n1=self.tors[0], p1='e1/54', po1='po54', n2=self.tors[-1], p2='e1/1', po2='po1')
        Link(n1=self.tors[1], p1='e1/54', po1='po54', n2=self.tors[-1], p2='e1/2', po2='po1')
        Link(n1=self.tors[2], p1='e1/54', po1='po54', n2=self.tors[-1], p2='e1/3', po2='po3')
        Link(n1=self.tors[3], p1='e1/54', po1='po54', n2=self.tors[-1], p2='e1/4', po2='po3')

        Link(n1=self.tors[0], p1='e1/1', po1='po10', n2=self.mgm, p2='MLOM')
        Link(n1=self.tors[1], p1='e1/1', po1='po10', n2=self.mgm, p2='MLOM')

        Link(n1=self.tors[0], p1='e1/21', po1='po21', n2=self.hosts[0], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/21', po1='po21', n2=self.hosts[0], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/22', po1='po22', n2=self.hosts[1], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/22', po1='po22', n2=self.hosts[1], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/23', po1='po23', n2=self.hosts[2], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/23', po1='po23', n2=self.hosts[2], p2='MLOM')
        Link(n1=self.tors[2], p1='e1/7', po1='po7', n2=self.hosts[3], p2='MLOM')
        Link(n1=self.tors[3], p1='e1/7', po1='po7', n2=self.hosts[3], p2='MLOM')

        Link(n1=self.tors[0], p1='e1/11', po1='po11', n2=self.hosts[4], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/11', po1='po11', n2=self.hosts[4], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/12', po1='po12', n2=self.hosts[5], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/12', po1='po12', n2=self.hosts[5], p2='MLOM')
        Link(n1=self.tors[2], p1='e1/17', po1='po17', n2=self.hosts[6], p2='MLOM')
        Link(n1=self.tors[3], p1='e1/17', po1='po17', n2=self.hosts[6], p2='MLOM')

        Link(n1=self.tors[0], p1='e1/31', po1='po31', n2=self.hosts[-5], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/31', po1='po31', n2=self.hosts[-5], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/32', po1='po32', n2=self.hosts[-4], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/32', po1='po32', n2=self.hosts[-4], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/33', po1='po32', n2=self.hosts[-3], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/33', po1='po32', n2=self.hosts[-3], p2='MLOM')

        Link(n1=self.tors[0], p1='e1/41', po1='po41', n2=self.hosts[-2], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/41', po1='po41', n2=self.hosts[-2], p2='MLOM')
        Link(n1=self.tors[0], p1='e1/42', po1='po42', n2=self.hosts[-1], p2='MLOM')
        Link(n1=self.tors[1], p1='e1/42', po1='po42', n2=self.hosts[-1], p2='MLOM')

        self.nets_d = {'a': Net(name='api', vlan_id=101, cidr='10.0.0.30/27'),
                       't': Net(name='ten', vlan_id=122, cidr='1.0.2.0/24'),
                       'm': Net(name='mx',  vlan_id=1400, cidr='10.20.30.0/24'),
                       'e': Net(name='ext', vlan_id=1401, cidr='10.20.40.0/24'),
                       'p': Net(name='pro', vlan_id=1402, cidr='10.20.50.0/24'),}


if __name__ == '__main__':
    plot_topology(pod=Pod())
    #graph_topo()
