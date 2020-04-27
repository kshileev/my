import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

with open('uuid-1773f78c-32eb-46cd-9b7b-454c7347f3b9.log') as f:
    body = f.read()
log_records = [x for x in body.split('\n') if x]

df = pd.DataFrame(dict(time=[x.split()[1] for x in log_records],
                       node=[x.split('/')[2] for x in log_records],
                       file=[x.split('/')[3].split(':')[0] for x in log_records],
                       msg=log_records
                       ))

fig = px.scatter(df, x='time', y='node', title='Server on comp2', color='file')
app = dash.Dash(name='kir')
app.layout = html.Div(children=[dcc.Graph(id='graph_id', figure=fig),
                                html.Pre(id='msg_id', children='some text')])

@app.callback(Output('msg_id', 'children'), [Input('graph_id', 'clickData')])
def update_msg(data_d):
    if data_d is None:
        return ''
    timestamp = data_d['points'][0]['x']
    msgs = [x.replace(' ', '\n').replace(',', ',\n') for x in df[df.time == timestamp].msg]
    msg = '\n\n******* Next log message with the same timestamp ******\n\n'.join(msgs)
    return f'at {timestamp} {len(msgs)} msg:\n{msg}'


app.run_server()
