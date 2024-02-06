from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly_express as px
from helpers import co2_ppm_df

df = co2_ppm_df()

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    # html.Div(children='Hello World & Ben'),
    # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    # dcc.Graph(figure=px.line(df, x='date', y=['average', 'deseasonalized'])),
    dcc.Graph(id='graph-content', style={'width': '90vh', 'height': '90vh'}),
    dcc.Dropdown(df.type_group.unique().tolist(), 'Actual values', id='dropdown-selection'),

])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.type_group==value]#.groupby(['date', 'variable']).sum().reset_index().pivot(index='date', values='value',  columns='variable').reset_index()
    fig = px.line(
        dff, 
        x='date', 
        y='value', 
        color='variable',
        labels={'average': 'Average monthly value'}
        ).update_layout(
            xaxis_title='Date',
            legend={'title': 'Measure'},
            title='Atmospheric CO2 concentrations'
        )
    if value == 'Actual values':
        fig.update_layout(yaxis_title='CO2 parts per million')
    else:
        fig.update_layout(yaxis_title='Year-on-year change in CO2 PPM')
    return fig

if __name__ == '__main__':
    
    app.run()
