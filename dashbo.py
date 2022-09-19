import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from connect_with_database import DatabaseConnect
from readDatabase import ReadData
from geography_lat_long import lat_and_long
from datetime import datetime
from dash.exceptions import PreventUpdate
from cardKpi import CardKpi, CardKpiTwo, CardKpiTree
from dropdownSelect import SelectDropdown
from pandas import DataFrame
from pie_graphs import PieChart, PieChartTwo
from bar_chart import BarChart
from line_chart import LineChart


card_kpi_1 = CardKpi('offert.db')
card = card_kpi_1.query_connection('property')

dropdown_select = SelectDropdown('offert.db')
dropdown_select.query_connection('property')


app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(src=app.get_asset_url('analytics.png'),
                     id='logo-image',
                     style={'height': '70px',
                            'width': 'auto',
                            'margin-bottom': '25px',
                            'margin-left': '5px'},
                     className='title_image'
                     ),

        html.H3('Data analysis flats and houses',
                style={'margin-bottom': '-5px',
                       'margin-left': '5px',
                       'color':'white'},
                className='title')
        ], className='logo_title'),
    ], id='header', className='row flex-display', style={'margin-buttom': '25px'}),

    html.Div(children=[
        html.Div([
            html.H6(children='Total add',
                    style={'textAlign': 'center',
                           'color': 'white',
                           'fontSize': 20
                           }),
            html.Img(src=app.get_asset_url('calculator.png'),
                     style={'height': '40px', 'marginTop': 20},
                     className='calculator'),

            html.H6(f'{card_kpi_1.count_totat_add()}',
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 20,
                           'textAlign': 'center'
                           },
                    className='count_add')

        ], className='card_container three column', style={'textAlign': 'center'}),


    html.Div(children=[
        html.Div(id='text_row2', style={'text-align': 'center'})

           ], className='card_container three column'),


    html.Div(children=[
                html.Div(id='text_row3')
           ], className='card_container three column', style={'textAlign': 'center'}),

    html.Div(children=[
        html.H6(id='get_date_time',
                style={'color': 'white'},
                className='adjust_date_time'),
           ], className='card_container three column', style={'textAlign': 'center'}),

    ], className='row flex-display'),

html.Div([
        dcc.Interval(id = 'update_date_time',
                     interval = 1000,
                     n_intervals = 0)
    ]),

    html.Div([
        dcc.Interval(id = 'update_value',
                     interval = 5000,
                     n_intervals = 0)
    ]),

    html.Div([
        html.Div([
            html.P('Select City:', style={'textAlign': 'center',
                                          'color':'white',
                                          'fontSize': 20}),
            dcc.Dropdown(id='w_city',
                         multi=False,
                         value='All',
                         placeholder='Select City',
                         options = [{'label': c, 'value':c}
                                    for c in dropdown_select.show_city_dropdown()], className='dcc_compon'
                         ),

            html.P('Select kind of investment:', style={'textAlign': 'center',
                                          'color':'white',
                                          'fontSize': 20}),
            dcc.Dropdown(id='w_kind_of_investment',
                         multi=False,
                         value='All',
                         placeholder='Select kind of investition',
                         options = [{'label': c, 'value':c}
                                    for c in dropdown_select.show_kind_of_investment_dropdown()], className='dcc_compon'
                         ),

            html.P('Select market:', style={'textAlign': 'center',
                                          'color':'white',
                                          'fontSize': 20}),
            dcc.Dropdown(id='w_market',
                         multi=False,
                         value='All',
                         placeholder='Select market',
                         options = [{'label': c, 'value':c}
                                    for c in dropdown_select.show_market_dropdown()], className='dcc_compon'
                         )

        ], className='create_container two columns'),

        html.Div([
            dcc.Graph(id ='pie_chart', config={'displayModeBar': 'hover'}
                      )

        ], className='create_container five columns'),

        html.Div([
            dcc.Graph(id ='pie_chart_two', config={'displayModeBar': 'hover'}
                      )

        ], className='create_container five columns'),

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id = 'bar_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container six column'),

        html.Div([
            dcc.Graph(id = 'line_chart',
                      config = {'displayModeBar': False},
                      className = 'line_chart_size')
        ], className = 'create_container six column')

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container1 twelve column')

    ], className='row flex-display')

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(Output('text_row2', 'children'),
              Input('w_city','value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value')
              )
def update_row2(w_city, w_kind_of_investment, w_market):
    data = CardKpiTwo('offert.db')
    data.query_connection('property')
    data.fill_in_the_data()

    average = data.average_price(w_city, w_kind_of_investment, w_market)

    return [
        html.Div([
               html.H6(children='Average price [PLN]',
                       style={'textAlign': 'center',
                              'color': 'white',
                              'fontSize': 20
                              }),
               html.Img(src=app.get_asset_url('price.png'),
                       style={'height': '40px','marginTop': 20},
                       className='price'),

               html.H6('{0:,.0f}'.format(average),
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 18,
                           'textAlign': 'center'
                           },
                    className='price'),
           ],className = 'price')
        ]

@app.callback(Output('text_row3', 'children'),
              Input('w_city','value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value')
              )
def update_row3(w_city, w_kind_of_investment, w_market):
    data = CardKpiTree('offert.db')
    data.query_connection('property')
    data.fill_in_the_data()
    kind, area, link = data.top_two_offert(w_city, w_kind_of_investment, w_market)

    return [
        html.Div([
               html.H6(children='Top 2 offert:',
                       style={'textAlign': 'center',
                              'color': 'white',
                              'fontSize': 18
                              }),
               html.Img(src=app.get_asset_url('topstar.png'),
                       style={'height': '40px','marginTop': 20},
                       className='price'),

            html.A(
                href=link[0],
                children=[
                    html.H6(f'{kind[0]} {area[0]} {"m²"} ',
                            style={'color': 'white',
                                   'font-weight': 'bold',
                                   'fontSize': 18,
                                   'textAlign': 'center',
                                   'text-decoration': 'none'
                                   },
                            className='link'
                    )
                ],
            ),

            html.A(
                href=link[1],
                children=[
                    html.H6(f'{kind[1]} {area[1]} {"m²"} ',
                            style={'color': 'white',
                                   'font-weight': 'bold',
                                   'fontSize': 18,
                                   'textAlign': 'center',
                                   'text-decoration': 'none'
                                   },
                            className='link'
                            )
                ],
            ),
        ], className='top_offert')
    ]

@app.callback(Output('get_date_time', 'children'),
              [Input('update_date_time', 'n_intervals')])
def live_date_time(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        time_string = now.strftime("%H:%M:%S")

    return [
        html.Div([
               html.H6(children='Date & time',
                       style={'textAlign': 'center',
                              'color': 'white',
                              'fontSize': 18
                              }),
               html.Img(src=app.get_asset_url('date.png'),
                       style={'height': '40px','marginTop': 20},
                       className='price'),

               html.H6(f'{time_string}',
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 18,
                           'textAlign': 'center'
                           },
                    className='time_string'),

                html.H6(f'{date_string}',
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 18,
                           'textAlign': 'center'
                           },
                    className='time_string'),
           ],className = 'date_time')
        ]

@app.callback(Output('pie_chart', 'figure'),
              Input('w_city','value'),
              Input('w_kind_of_investment','value'),
              Input('w_market','value')
              )
def update_graph(w_city, w_kind_of_investment, w_market):
    filtered_data = PieChart('offert.db')
    filtered_data.query_connection('property')
    filtered_data.fillna('nieznany', 'market')
    data = filtered_data.get_data_to_graph(w_city, w_kind_of_investment, w_market)
    ind = data.index
    colors = [ '#dd1e35', '#778899']

    return {
        'data': [go.Pie(
            labels=[data.loc[k]['kind_of_investment'] for k in ind],
            values=[data.loc[k]['id'] for k in ind],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=15,
            insidetextorientation= 'radial',
        )],

        'layout': go.Layout(
            title={'text': 'Advertisements: ' + (w_city),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 18},
            font=dict(family='sans-serif',
                      color='white',
                      size=18),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.2}
        )
    }

@app.callback(Output('pie_chart_two', 'figure'),
              Input('w_city','value'),
              Input('w_kind_of_investment','value'),
              Input('w_market','value'))
def update_graph_two(w_city, w_kind_of_investment, w_market):
    filtered_data = PieChartTwo('offert.db')
    filtered_data.query_connection('property')
    filtered_data.fillna('nieznany', 'market')
    data = filtered_data.get_data_to_graph(w_city, w_kind_of_investment, w_market)
    ind = data.index
    colors = ['green']

    return {
        'data': [go.Pie(
            labels=[data.loc[k]['market'] for k in ind],
            values=[data.loc[k]['id'] for k in ind],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=15,
            insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'Market: ' + (w_kind_of_investment),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 18},
            font=dict(family='sans-serif',
                      color='white',
                      size=18),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.2}
        )
    }

@app.callback(Output('bar_chart', 'figure'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value'))
def update_graph(w_city, w_kind_of_investment, w_market):
    df = BarChart('offert.db')
    df.query_connection('property')
    df.fillna('nieznany', 'market')
    df.convert_date('date_addition_add', format='%Y-%m', strformat='%Y-%B')
    offert = df.show_bar_chart(w_city, w_kind_of_investment, w_market)

    return {
        'data': [go.Bar(
            x=offert['date_addition_add'],
            y=offert['id'],
            name='Monthly Add',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>Date additional add</b>: ' + offert['date_addition_add'] + '<br>' +
            '<b>Offert</b>: ' + [f'{x:,.0f}' for x in offert['id']] + '<br>'
        ),
        ],

        'layout': go.Layout(
            title={'text': 'When advertisements were add: ' + (w_city),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 16},
            font=dict(family='sans-serif',
                      color='white',
                      size=16),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=20, t=30, b=110, l=90),
            xaxis=dict(title='Date',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=16
                       )),
            yaxis=dict(title='Number of offers',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=16
                       )
                       )
        )
    }

@app.callback(Output('line_chart', 'figure'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value'))
def update_graph(w_city, w_kind_of_investment, w_market):
    df = LineChart('offert.db')
    df.query_connection('property')
    price_per_1m2 = df.price_per_m2()
    df.insert_column(6, 'price_per_1m2', price_per_1m2)
    df.fillna('nieznany', 'market')
    df.fillna('nieznany', 'kind_of_investment')
    df.convert_date('date_addition_add', format='%Y-%m', strformat='%Y-%B')
    data = df.show_line_chart(w_city, w_kind_of_investment, w_market)
    text_color = np.where(data['price_per_1m2'] > 0, 'white', '#FF3399')

    return {
        'data': [
            go.Scatter(
                x = data['date_addition_add'],
                y = data['price_per_1m2'],
                text = data['price_per_1m2'],
                texttemplate = '' + '%{text:,.0f}',
                textposition = 'top center',
                textfont = dict(
                    family = "Calibri",
                    size = 16,
                    color = text_color,
                ),
                mode = 'markers+lines+text',
                line = dict(shape = "spline", smoothing = 1.3, width = 3, color = '#B258D3'),
                marker = dict(size = 10, symbol = 'circle', color = 'white',
                              line = dict(color = '#00B0F0', width = 2)
                              ),
                hoverinfo = 'text',
                hovertext =
                '<b>Date additional add</b>: ' + data['date_addition_add'] + '<br>' +
                '<b>Offert</b>: ' + [f'{x:,.0f}' for x in data['price_per_1m2']] + '<br>'
            )],

        'layout': go.Layout(
            title={'text': 'Price average: ' + (w_city),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            titlefont={'color': 'white',
                       'size': 16},
            font=dict(family='sans-serif',
                      color='white',
                      size=16),
            margin = dict(r = 20, t = 30, b = 110, l = 90),
            xaxis = dict(title = 'Date',
                         visible = True,
                         color = 'white',
                         showline = False,
                         showgrid = False,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Aerial',
                             size = 16,
                             color = 'white'),
                         range=[datetime(2020, 12, 31), datetime(2022, 5,31)],
                         ),

            yaxis = dict(title = 'Price for 1m2',
                         tickprefix = ' ',
                         tickformat = ',.0f',
                         visible = True,
                         color = 'white',
                         showline = False,
                         showgrid = False,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Aerial',
                             size = 16,
                             color = 'white'),
                         # range=[6000, 15000],
                         ),

        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
