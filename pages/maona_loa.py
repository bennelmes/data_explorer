import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly_express as px
from pages.helpers import co2_ppm_df

dash.register_page(__name__)

df = co2_ppm_df()

max_date = df.date.max().strftime('%B %Y')
latest_ppm = df[(df.date == df.date.max()) & (df.variable == 'Seasonally adjusted')].value.tolist()[0]
latest_ppm_change = round(df[(df.variable == 'Seasonally adjusted')].value.diff(12).tolist()[-1], ndigits=2)
month_max_ppm = df[(df.variable == 'Seasonally adjusted') & (df.value == df[df.variable == 'Seasonally adjusted'].value.max())].date.tolist()[0].strftime('%B %Y')

# Create app layout

layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(html.P(''), align='center'),
                    dbc.Row(html.P('Select the type of data to display'), align='center'),
                    dbc.Row(dcc.RadioItems(df.type_group.unique().tolist(), 'Actual values', id='dropdown-selection', style={'font': 'Arial'}), align='center'),
                    dbc.Row(html.P(''), align='center'),
                    dbc.Row(html.P('At {m}, atmospheric CO2 concentrations were at {ppm} ppm'.format(m=max_date, ppm=latest_ppm)), align='center'),                
                    dbc.Row(html.P('This was {ppmc} ppm higher than the same month in the previous year.'.format(ppmc=latest_ppm_change), style={'color': 'red'}), align='center'),
                    dbc.Row(html.P('The record for the highest seasonally adjusted CO2 concentration was last broken in {}.'.format(month_max_ppm)), align='center'),
                ],
                width = 2
                ),
            dbc.Col(
                [
                    dbc.Row(dcc.Graph(id='graph-content', style={'width': '800', 'height': '500', 'autosize': False}), align='right'),
                ],
                width = 8
                )
        ]
    ),
    dbc.Row(dbc.Row(html.P('Source: Maona Loa Observatory, Dr. Pieter Tans, NOAA/GML (gml.noaa.gov/ccgg/trends/) and Dr. Ralph Keeling, Scripps Institution of Oceanography (scrippsco2.ucsd.edu/).'), align='center')
)
]
)


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
            title='Monthly average CO2 concentrations at Maona Loa Observatory, Hawaii, USA'
        )
    if value == 'Actual values':
        fig.update_layout(yaxis_title='CO2 parts per million')
    else:
        fig.update_layout(yaxis_title='Year-on-year change in CO2 PPM')
    return fig

