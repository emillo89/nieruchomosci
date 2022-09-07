import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from connect_with_database import DatabaseConnect
from readDatabase import ReadData
from geography_lat_long import lat_and_long


df = ReadData('offert.db')
con = df.query_connection()

'''1. How many add in database'''
total_count = df.count_totat_add()

'''2. Kind of investments'''
houses = df.count_houses()
flats = df.count_flats()
# print(houses)

'''3. Select city dropdown'''
city = df.show_city_dropdown()
city = np.append(city, 'All')

'''4. Select market dropdown'''
kind_investition = df.show_kind_of_investment_dropdown()
kind_investition= np.append(kind_investition, 'All')
print(kind_investition)

'''5. Select market dropdown'''

market = df.show_market_dropdown()
market = np.append(market, 'All')
# market = ['pierwotny', 'wtórny', 'nieznany', 'All']
print(market)

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(src=app.get_asset_url('analytics.png'),
                     id='logo-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'}

                     )
        ], className='one-third column'),

        html.Div(children=[
            html.Div([
                html.H3('Data analysis flats and houses', style={'margin-bottom': '0px', 'color':'white'})

            ])

        ], className='one-half column', id='title'),

    ], id='header', className='row flex-display', style={'margin-buttom': '25px'}),

    html.Div(children=[
           html.Div(children=[
                html.H6(children='Total add',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 40}),
                html.P(f'Houses: {houses}',
                        style={'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15}),
                html.P(f'Flats: {flats}',
                        style={'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15}),
           ], className='card_container three columns'),

    html.Div(children=[
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': '#dd1e35',
                               'fontSize': 40}),
           ], className='card_container three columns'),


    html.Div(children=[
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': 'green',
                               'fontSize': 40}),
           ], className='card_container three columns'),

    html.Div(children=[
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': '#e55467',
                               'fontSize': 40}),
           ], className='card_container three columns')

    ], className='row flex-display'),

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
                                    for c in city], className='dcc_compon'
                         ),

            html.P('Select kind of investment:', style={'textAlign': 'center',
                                          'color':'white',
                                          'fontSize': 20}),
            dcc.Dropdown(id='w_kind_of_investment',
                         multi=False,
                         value='All',
                         placeholder='Select kind of investition',
                         options = [{'label': c, 'value':c}
                                    for c in kind_investition], className='dcc_compon'
                         ),

            html.P('Select market:', style={'textAlign': 'center',
                                          'color':'white',
                                          'fontSize': 20}),
            dcc.Dropdown(id='w_market',
                         multi=False,
                         value='All',
                         placeholder='Select market',
                         options = [{'label': c, 'value':c}
                                    for c in market], className='dcc_compon'
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
        ], className='create_container six columns'),

    html.Div([
        dcc.Graph(id = 'line_chart',
                  config = {'displayModeBar': False},
                  className = 'line_chart_size')
    ], className = 'create_container six columns')

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container1 twelve columns')

    ], className='row flex-display')

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


def connection():
    data_reader = ReadData('offert.db')
    df = data_reader.query_connection()
    return df

def inny():
    df = ReadData('offert.db')
    con = df.query_connection()
    return df.df

# print('-----')
# print(inny())

def add_column_lat_long(geography_lat_long):
    df = connection()
    cities = df['city'].unique()

    for city in cities:
        if city in geography_lat_long:
            df.loc[df['city'] == city, 'lat'] = geography_lat_long[city]['lat']
            df.loc[df['city'] == city, 'long'] = geography_lat_long[city]['long']
    print(df)
    return df


@app.callback(Output('pie_chart', 'figure'),
              Input('w_city','value'),
              Input('w_kind_of_investment','value')
              )
def update_graph(w_city, w_kind_of_investment):
    df = connection()
    if w_city == 'All' and w_kind_of_investment == 'All':
        filtered_df = df.groupby('kind_of_investment').agg({'id': pd.Series.count}).reset_index()
        data = filtered_df
    elif w_city == 'All' and w_kind_of_investment != 'All':
        filtered_df = df.groupby('kind_of_investment').agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        print(data)
    elif w_city != 'All' and w_kind_of_investment != 'All':
        filtered_df = df.groupby(['city', 'kind_of_investment'])[['id']].count().reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
    else:
        filtered_df = df.groupby(['city', 'kind_of_investment'])[['id']].count().reset_index()
        data = filtered_df[(filtered_df['city'] == w_city)]

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
            insidetextorientation= 'radial'

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
    df = connection()
    # df = df.query_connection()
    df['market'].fillna('nieznany', inplace=True)
    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby('market').agg({'id': pd.Series.count}).reset_index()
        data = filtered_df
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['market','kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        print(data)
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby(['market','city']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city)]
    elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['market'] == w_market)]
    elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['market','city', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['market','city']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
        filtered_df = df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
    else:
        filtered_df = df.groupby(['city', 'kind_of_investment', 'market'])[['id']].count().reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]

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
    df = connection()
    # df = df.query_connection()
    df['market'].fillna('nieznany', inplace=True)
    df['date_addition_add'] = (pd.to_datetime(df['date_addition_add'], format='%Y-%m').dt.strftime('%Y-%B'))
    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        offert = df.groupby(['date_addition_add'], as_index=False).agg({'id':pd.Series.count}).sort_values('date_addition_add')
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add', 'city']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['city'] == w_city)]
        print(offert)
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['city'] == w_kind_of_investment)]
    elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'market']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['market'] == w_market)]
    elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add','city', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'kind_of_investment', 'market']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'city', 'market']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
    else:
        filtered_df = df.groupby(['date_addition_add', 'city', 'kind_of_investment', 'market']).agg({'id': pd.Series.count}).reset_index()
        offert = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]

    return {
        'data': [go.Bar(
            x=offert['date_addition_add'],
            y=offert['id'],
            name='Monthly Add',
            marker=dict(color='orange'),
            hoverinfo='text',

            # hovertext=
            # '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            # '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            # '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'


        ),
        ],

        'layout': go.Layout(
            title={'text': 'When advertisements were add: ' + (w_city),
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
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
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
    df = connection()
    price_per_1m2 = (df['price'] // df['area']).apply(np.ceil)
    df.insert(6, 'price_per_1m2', price_per_1m2)




    df['price_per_1m2'].fillna('nieznany', inplace=True)
    df['date_addition_add'] = (pd.to_datetime(df['date_addition_add'], format='%Y-%m').dt.strftime('%Y-%B'))
    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        data = df.groupby(['date_addition_add'], as_index=False).agg({'price_per_1m2': pd.Series.mean})
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add', 'kind_of_investment']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add', 'city']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city)]
    elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[(filtered_df['market'] == w_market)]
    elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['date_addition_add', 'city', 'kind_of_investment']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'city', 'market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
        filtered_df = df.groupby(['date_addition_add', 'kind_of_investment', 'w_market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[
            (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
    else:
        filtered_df = df.groupby(['date_addition_add', 'city', 'kind_of_investment', 'market']).agg(
            {'price_per_1m2': pd.Series.mean}).reset_index()
        data = filtered_df[
            (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                        filtered_df['market'] == w_market)]
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
                    size = 18,
                    color = text_color,
                ),
                mode = 'markers+lines+text',
                line = dict(shape = "spline", smoothing = 1.3, width = 3, color = '#B258D3'),
                marker = dict(size = 10, symbol = 'circle', color = 'white',
                              line = dict(color = '#00B0F0', width = 2)
                              ),

                hoverinfo = 'text',
                # hovertext =
                # '<b>Month</b>: ' + months.astype(str) + '<br>' +
                # '<b>Net Profit</b>: $' + [f'{x:,.0f}' for x in net_profit] + '<br>'
            )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            titlefont={'color': 'white',
                       'size': 18},
            font=dict(family='sans-serif',
                      color='white',
                      size=18),
            margin = dict(r = 20, t = 20, b = 70, l = 90),
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
                             size = 14,
                             color = 'white')
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
                             size = 14,
                             color = 'white')
                         ),
        )
    }


@app.callback(Output('map_chart', 'figure'),
              Input('w_city', 'value'))
def update_graph(w_city):
    df = add_column_lat_long(lat_and_long)

    if w_city:
        geograp = df.groupby(['city','lat','long'])[[ 'id']].agg({'id': pd.Series.count}).reset_index()
        geography = geograp[geograp['city']==w_city]
        print(geography)
# geography2 =
# if w_city:
        zoom=3
        zoom_lat = float(geography['lat'])
        zoom_long = float(geography['long'])
        print(f'{zoom_lat} - {zoom_long}asdadadad')
# 'Warszawa': {'lat': '52.229675', 'long': '52.229675'},

    return {
        'data': [go.Scattermapbox(
            lon=geography['long'],
            lat=geography['lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=geography['id'],
                                           color=geography['id'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            # hoverinfo='text',
            # hovertext=
            # '<b>Region</b>: ' + terr9['region_txt'].astype(str) + '<br>' +
            # '<b>Country</b>: ' + terr9['country_txt'].astype(str) + '<br>' +
            # '<b>Province/State</b>: ' + terr9['provstate'].astype(str) + '<br>' +
            # '<b>City</b>: ' + terr9['city'].astype(str) + '<br>' +
            # '<b>Year</b>: ' + terr9['iyear'].astype(str) + '<br>' +
            # '<b>Death</b>: ' + [f'{x:,.0f}' for x in terr9['nkill']] + '<br>' +
            # '<b>Injured</b>: ' + [f'{x:,.0f}' for x in terr9['nwound']] + '<br>' +
            # '<b>Attack</b>: ' + [f'{x:,.0f}' for x in terr9['attacktype1']] + '<br>'


        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#010915',
            plot_bgcolor='#010915',
            margin=dict(r=0, l =0, b = 0, t = 0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiZW1pbGxvODkiLCJhIjoiY2w3bnNjN2cyMG83eDN1bzB2OHB6NGh2OSJ9.FoBvs_PL6PdhytI3OGE2DA',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                # style='open-street-map',
                zoom=3,
            ),



        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)

