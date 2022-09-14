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

# data_preparator = DataPreparator()
# data_preparator.prepare_data()
 ########
df = ReadData('offert.db')
con = df.query_connection()

'''1.1 How many add in database'''
total_count = df.count_totat_add()
'''1.2 Average per 1m2'''
price_average = df.price_per_m2()

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

            html.H6(f'{total_count}',
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


def connection():
    data_reader = ReadData('offert.db')
    df = data_reader.query_connection()
    return df

def inny():
    df = ReadData('offert.db')
    con = df.query_connection()
    return df.df

def add_column_lat_long(geography_lat_long):
    df = connection()
    cities = df['city'].unique()

    for city in cities:
        if city in geography_lat_long:
            df.loc[df['city'] == city, 'lat'] = geography_lat_long[city]['lat']
            df.loc[df['city'] == city, 'long'] = geography_lat_long[city]['long']
    print(df)
    return df

@app.callback(Output('text_row2', 'children'),
              Input('w_city','value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value')
              )
def update_row2(w_city, w_kind_of_investment, w_market):
    df = connection()
    price_per_1m2 = (df['price'] // df['area']).apply(np.ceil)
    df.insert(6, 'price_per_1m2', price_per_1m2)
    df['market'].fillna('nieznany', inplace=True)
    df['kind_of_investment'].fillna('nieznany', inplace=True)

    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        average = df.agg({'price_per_1m2': pd.Series.mean})['price_per_1m2']
    else:
        if w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = df.groupby(['city']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[filtered_df['city'] == w_city][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = df.groupby(['kind_of_investment']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[filtered_df['kind_of_investment'] == w_kind_of_investment][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = df.groupby(['market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[filtered_df['market'] == w_market][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment !=   'All' and w_market == 'All':
            filtered_df = df.groupby(['city', 'kind_of_investment']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[(filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = df.groupby(['kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[
                    (filtered_df['market'] == w_market) & (filtered_df['kind_of_investment'] == w_kind_of_investment)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = df.groupby(['city', 'market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[
                    (filtered_df['market'] == w_market) & (filtered_df['city'] == w_city)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = df.groupby(['city', 'kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[(filtered_df['city'] == w_city) &
                                        (filtered_df['kind_of_investment'] == w_kind_of_investment) &
                                        (filtered_df['market'] == w_market)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']


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
    df = connection()
    price_per_1m2 = (df['price'] // df['area']).apply(np.ceil)
    df.insert(6, 'price_per_1m2', price_per_1m2)
    df['market'].fillna('nieznany', inplace=True)
    df['kind_of_investment'].fillna('nieznany', inplace=True)

    top3 = df.sort_values('price_per_1m2')[['id', 'kind_of_investment', 'city', 'market', 'area', 'price_per_1m2', 'price', 'link']]

    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        kind = [k for k in top3.head(3)['kind_of_investment']]
        area = [k for k in top3.head(3)['area']]
        link = [k for k in top3.head(3)['link']]
    else:
        if w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = top3.loc[top3['city'] == w_city]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = top3.loc[top3['kind_of_investment'] == w_kind_of_investment]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = top3.loc[top3['market'] == w_market]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = top3.loc[(top3['city'] == w_city) & (top3['kind_of_investment'] == w_kind_of_investment)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = top3.loc[(top3['market'] == w_market) & (top3['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = top3.loc[(top3['city'] == w_city) & (top3['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = top3.loc[(top3['city'] == w_city) & (top3['kind_of_investment'] == w_kind_of_investment) & (top3['market'] == w_market)]

        try:
            kind = [k for k in filtered_df.head(3)['kind_of_investment']]
        except IndexError:
            kind = None
        try:
            area = [k for k in filtered_df.head(3)['area']]
        except IndexError:
            area = 0
        try:
            link = [k for k in filtered_df.head(3)['link']]
        except IndexError:
            link = None

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
    df = connection()
    df['market'].fillna('nieznany', inplace=True)
    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby('kind_of_investment').agg({'id': pd.Series.count}).reset_index()
        data = filtered_df
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        print(data)
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        filtered_df = df.groupby(['kind_of_investment', 'city']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city)]
    elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['market'] == w_market)]
    elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
        filtered_df = df.groupby(['city', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[
            (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
    elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
        filtered_df = df.groupby(['kind_of_investment', 'city', 'market']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
    elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
        filtered_df = df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
        data = filtered_df[
            (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
    else:
        filtered_df = df.groupby(['city', 'kind_of_investment', 'market'])[['id']].count().reset_index()
        data = filtered_df[
            (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                        filtered_df['market'] == w_market)]

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
    df = connection()
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
        offert = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
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
    df = connection()
    price_per_1m2 = (df['price'] // df['area']).apply(np.ceil)
    df.insert(6, 'price_per_1m2', price_per_1m2)
    df['market'].fillna('nieznany', inplace=True)
    df['kind_of_investment'].fillna('nieznany', inplace=True)
    df['price_per_1m2'].fillna('nieznany', inplace=True)
    df = df.sort_values('date_addition_add')
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
        filtered_df = df.groupby(['date_addition_add', 'kind_of_investment', 'market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
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
                             size = 16,
                             color = 'white'),
                         range=['2021-12', '2022-05'],
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

@app.callback(Output('map_chart', 'figure'),
              Input('w_city', 'value'),
              Input('w_kind_of_investment', 'value'),
              Input('w_market', 'value'))
def update_graph(w_city, w_kind_of_investment, w_market):
    df = add_column_lat_long(lat_and_long)
    df['market'].fillna('nieznany', inplace=True)
    df['kind_of_investment'].fillna('nieznany', inplace=True)

    if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
        geography = df.groupby(['city', 'lat', 'long'])[['id']].agg(
            {'id': pd.Series.count}).reset_index()
    else:
        if w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            geograp = df.groupby(['city', 'kind_of_investment', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[geograp['kind_of_investment'] == w_kind_of_investment]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            geograp = df.groupby(['city', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[geograp['market'] == w_market]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            geograp = df.groupby(['city', 'kind_of_investment', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            geograp = df.groupby(['city', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['city'] == w_city)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            geograp = df.groupby(['city', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['market'] == w_market) & (geograp['city'] == w_city)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            geograp = df.groupby(['city', 'kind_of_investment', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['city'] == w_city)]
        else:
            geograp = df.groupby(['city', 'kind_of_investment','market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[
                (geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['city'] == w_city) & (geograp['market'] == w_market)]
    zoom_lat = float(52.229675)
    zoom_long = float(21.012230)
    zoom = 5
    print(f'{zoom_lat} - {zoom_long}asdadadad')

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
            margin=dict(r=0, l =0, b = 0, t = 0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiZW1pbGxvODkiLCJhIjoiY2w3bnNjN2cyMG83eDN1bzB2OHB6NGh2OSJ9.FoBvs_PL6PdhytI3OGE2DA',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)

