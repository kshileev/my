from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import pandas as pd
import plotly.express as px

time = []
name = []
status = []
text = []
with open(os.path.expanduser(os.path.join('~', 'repo', 'testrepo', 'lib', 'unittests', 'log_sqe_mon.txt'))) as f:
    for line in f:
        if line.count('|') != 4:
            continue
        splitted = line.split('|')
        if splitted[2].strip() not in ['PASSED', 'FAILED']:
            continue
        time.append(dt.strptime(splitted[0].strip(), '%d %b %Y %H:%M:%S %Z'))
        name.append(splitted[1].strip())
        status.append(splitted[2].strip())
        text.append(line)


df = pd.DataFrame(dict(time=time, object=name, status=status, text=text))

fig = px.scatter(df, x='time', y='object', title='Performance', color='status')
app = dash.Dash(name='kir')
app.layout = html.Div(children=[dcc.Graph(id='graph_id', figure=fig),
                                html.Pre(id='describe_id', children='')])

@app.callback(Output('describe_id', 'children'), [Input('graph_id', 'clickData')])
def update_msg(data_d):
    if data_d is None:
        return 'Click on data point to see description'
    timestamp = data_d['points'][0]['x']
    name = data_d['points'][0]['y']
    all_at_time = [x for x in df[df.time == timestamp].text]
    this_point = df[(df.time == timestamp) & (df.object == name)].text.values[0]
    return f'{this_point}\n\nTotal {len(all_at_time)} records at the same time:\n{"".join(all_at_time)}'


app.run_server()
