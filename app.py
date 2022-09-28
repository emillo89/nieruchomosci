import numpy as np
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
from dash.exceptions import PreventUpdate
from cardKpi import CardKpi, CardKpiTwo, CardKpiTree
from dropdownSelect import SelectDropdown
from pie_graphs import PieChart, PieChartTwo
from bar_chart import BarChart
from line_chart import LineChart
from map_chart import MapChart
from geography_lat_long import lat_and_long

card_kpi_1 = CardKpi('offert.db')
card = card_kpi_1.query_connection('property')

dropdown_select = SelectDropdown('offert.db')
dropdown_select.query_connection('property')

app = Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(src=app.get_asset_url('analytics.png'),
                     id='logo-image',
                     style={'height': '70px',
                            'width': 'auto',
                            'margin-bottom': '25px',
                            'margin-left': '5px'},
                     className='title_image scal'
                     ),

            html.H3('Data analysis flats and houses',
                    style={'margin-bottom': '-5px',
                           'margin-left': '2px',
                           'color': 'white',
                           'fontSize': 20},
                    className='title scal')
        ], className='logo_title'),
    ], id='header', className='row flex-display', style={'margin-buttom': '25px'}),

    html.Div(children=[
        html.Div([
            html.H6(children='Total add',
                    style={'textAlign': 'center',
                           'color': 'white',
                           'fontSize': 18,
                           'marginTop': 20
                           }, className='scal'),
            html.Img(src=app.get_asset_url('calculator.png'),
                     style={'height': '40px', 'marginTop': 8},
                     className='calculator scal'),

            html.H6(f'{card_kpi_1.count_totat_add()}',
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 18,
                           'textAlign': 'center',
                           'marginTop': -1
                           },
                    className='count_add scal')

        ], className='card_container three column', style={'textAlign': 'center'}),

        html.Div(children=[
            html.Div(id='text_row2', style={'text-align': 'center'}, className='scal')

        ], className='card_container three column'),

        html.Div(children=[
            html.Div(id='text_row3', className='scal')
        ], className='card_container three column', style={'textAlign': 'center'}),

        html.Div(children=[
            html.H6(id='get_date_time',
                    style={'color': 'white'},
                    className='adjust_date_time scal'),
        ], className='card_container three column', style={'textAlign': 'center'}),

    ], className='row flex-display'),

    html.Div([
        dcc.Interval(id='update_date_time',
                     interval=1000,
                     n_intervals=0)
    ]),

    html.Div([
        dcc.Interval(id='update_value',
                     interval=5000,
                     n_intervals=0)
    ]),

    html.Div([
        html.Div([
            html.P('Select City:', style={'textAlign': 'center',
                                          'color': 'white',
                                          'fontSize': 14}),
            dcc.Dropdown(id='w_city',
                         style={'fontSize': 14},
                         multi=False,
                         value='All',
                         placeholder='Select City',
                         options=[{'label': c, 'value': c}
                                  for c in dropdown_select.show_city_dropdown()], className='dcc_compon'
                         ),

            html.P('Select kind of investment:', style={'textAlign': 'center',
                                                        'color': 'white',
                                                        'fontSize': 14}),
            dcc.Dropdown(id='w_kind_of_investment',
                         style={'fontSize': 14},
                         multi=False,
                         value='All',
                         placeholder='Select kind of investition',
                         options=[{'label': c, 'value': c}
                                for c in dropdown_select.show_kind_of_investment_dropdown()], className='dcc_compon'
                         ),

            html.P('Select market:', style={'textAlign': 'center',
                                            'color': 'white',
                                            'fontSize': 14}),
            dcc.Dropdown(id='w_market',
                         style={'fontSize': 14},
                         multi=False,
                         value='All',
                         placeholder='Select market',
                         options=[{'label': c, 'value': c}
                                  for c in dropdown_select.show_market_dropdown()], className='dcc_compon'
                         )

        ], className='create_container two columns'),

        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'},
                      className='scal')

        ], className='create_container five columns'),

        html.Div([
            dcc.Graph(id='pie_chart_two', config={'displayModeBar': 'hover'},
                      className='scal')

        ], className='create_container five columns'),

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='bar_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container six column'),

        html.Div([
            dcc.Graph(id='line_chart',
                      config={'displayModeBar': False},
                      className='line_chart_size')
        ], className='create_container six column')

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container1 twelve column')

    ], className='row flex-display')

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('text_row2', 'children'),
              Input('w_city', 'value'),
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
                           'fontSize': 18
                           }),
            html.Img(src=app.get_asset_url('price.png'),
                     style={'height': '40px', 'marginTop': 20},
                     className='price'),

            html.H6('{0:,.0f}'.format(average),
                    style={'color': 'white',
                           'font-weight': 'bold',
                           'fontSize': 18,
                           'textAlign': 'center',
                           'marginTop': 10
                           },
                    className='price'),
        ], className='price')
    ]


@app.callback(Output('text_row3', 'children'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value')
              )
def update_row3(w_city, w_kind_of_investment, w_market):
    data = CardKpiTree('offert.db')
    data.query_connection('property')
    data.fill_in_the_data()
    kind, area, link = data.top_two_offert(w_city, w_kind_of_investment, w_market)

    if len(link) == 0 and len(kind) == 0 and len(area) == 0:
        link = ['','']
        kind = ['','']
        area = ['','']


    return [
        html.Div([
            html.H6(children='Top 2 offert:',
                    style={'textAlign': 'center',
                           'color': 'white',
                           'fontSize': 18
                           }),
            html.Img(src=app.get_asset_url('topstar.png'),
                     style={'height': '40px', 'marginTop': 20},
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
                     style={'height': '40px', 'marginTop': 20},
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
        ], className='date_time')
    ]


@app.callback(Output('pie_chart', 'figure'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value')
              )
def update_graph(w_city, w_kind_of_investment, w_market):
    filtered_data = PieChart('offert.db')
    filtered_data.query_connection('property')
    filtered_data.fillna('nieznany', 'market')
    data = filtered_data.get_data_to_graph(w_city, w_kind_of_investment, w_market)
    ind = data.index
    colors = ['#dd1e35', '#778899']

    return {
        'data': [go.Pie(
            labels=[data.loc[k]['kind_of_investment'] for k in ind],
            values=[data.loc[k]['id'] for k in ind],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=15,
            insidetextorientation='radial',
        )],

        'layout': go.Layout(
            title={'text': 'Advertisements: ' + w_city,
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
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value'))
def update_graph_two(w_city, w_kind_of_investment, w_market):
    filtered_data = PieChartTwo('offert.db')
    filtered_data.query_connection('property')
    filtered_data.fillna('nieznany', 'market')
    data = filtered_data.get_data_to_graph(w_city, w_kind_of_investment, w_market)
    ind = data.index
    colors = ['green', 'gold', 'purple']

    return {
        'data': [go.Pie(
            labels=[data.loc[k]['market'] for k in ind],
            values=[data.loc[k]['id'] for k in ind],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=15,
            insidetextorientation='radial'

        )],

        'layout': go.Layout(
            title={'text': 'Market: ' + w_kind_of_investment,
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
    # offert_year = df.take_year()
    # offert_month = df.take_month()
    df.convert_date('date_addition_add', format='%Y-%m', strformat='%Y-%B')
    # df.insert_column(22, 'year', offert_year)
    # df.insert_column(23, 'month', offert_month)

    offert = df.show_bar_chart(w_city, w_kind_of_investment, w_market)

    return {
        'data': [go.Bar(
            x=offert['date_addition_add'],
            y=offert['id'],
            name='Monthly Add',
            marker=dict(color='#00B0F0'),
            hoverinfo='text',
            hovertext=
            '<b>Date additional add</b>: ' + offert['date_addition_add'] + '<br>' +
            '<b>Offert</b>: ' + [f'{x:,.0f}' for x in offert['id']] + '<br>'
        ),
        ],

        'layout': go.Layout(
            title={'text': 'When advertisements were add: ' + w_city,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 14},
            font=dict(family='sans-serif',
                      color='white',
                      size=14),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=20, t=30, b=110, l=90),
            xaxis=dict(title='Date',
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
                           size=14
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
                           size=14
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
                x=data['date_addition_add'],
                y=data['price_per_1m2'],
                text=data['price_per_1m2'],
                texttemplate='' + '%{text:,.0f}',
                textposition='top center',
                textfont=dict(
                    family="Calibri",
                    size=14,
                    color=text_color,
                ),
                mode='markers+lines+text',
                line=dict(shape="spline", smoothing=1.3, width=3, color='#B258D3'),
                marker=dict(size=10, symbol='circle', color='white',
                            line=dict(color='#00B0F0', width=2)
                            ),
                hoverinfo='text',
                hovertext=
                '<b>Date additional add</b>: ' + data['date_addition_add'] + '<br>' +
                '<b>Offert</b>: ' + [f'{x:,.0f}' for x in data['price_per_1m2']] + '<br>'
            )],

        'layout': go.Layout(
            title={'text': 'Price average: ' + w_city,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            titlefont={'color': 'white',
                       'size': 14},
            font=dict(family='sans-serif',
                      color='white',
                      size=14),
            margin=dict(r=20, t=30, b=110, l=90),
            xaxis=dict(title='Date',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           size=14,
                           color='white'),
                       range=[datetime(2020, 12, 31), datetime(2022, 5, 31)],
                       ),

            yaxis=dict(title='Price for 1m2',
                       tickprefix=' ',
                       tickformat=',.0f',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           size=14,
                           color='white')
                       ),

        )
    }


@app.callback(Output('map_chart', 'figure'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value'))
def update_graph(w_city, w_kind_of_investment, w_market):
    df = MapChart('offert.db')
    df.query_connection('property')
    df.fillna('nieznany', 'market')
    df.fillna('nieznany', 'kind_of_investment')
    df.add_column_lat_long(lat_and_long)
    geography = df.show_map(w_city, w_kind_of_investment, w_market)
    zoom_lat = float(52.229675)
    zoom_long = float(21.012230)
    zoom = 5

    return {
        'data': [go.Scattermapbox(
            lon=geography['long'],
            lat=geography['lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=geography['id'] * 10,
                                           color=geography['id'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>City</b>: ' + geography['city'] + '<br>' +
            '<b>Latitude</b>: ' + geography['lat'] + '<br>' +
            '<b>Longitude</b>: ' + geography['long'] + '<br>' +
            '<b>Offert</b>: ' + [f'{x:,.0f}' for x in geography['id']] + '<br>'
        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#010915',
            plot_bgcolor='#010915',
            margin=dict(r=0, l=0, b=0, t=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiZW1pbGxvODkiLCJhIjoiY2w3bnNjN2cyMG83eDN1bzB2OHB6NGh2OSJ9.FoBvs_'
                            'PL6PdhytI3OGE2DA',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
