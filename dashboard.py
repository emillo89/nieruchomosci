import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from connect_with_database import DatabaseConnect
from readDatabase import ReadData



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

        ], className='create_container three columns'),

        html.Div([
            dcc.Graph(id ='pie_chart', config={'displayModeBar': 'hover'}
                      )

        ], className='create_container four columns'),

        html.Div([
            dcc.Graph(id ='pie_chart_two', config={'displayModeBar': 'hover'}
                      )

        ], className='create_container four columns'),

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container six columns'),

    ], className='row flex-display')

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


def connection():
    data_reader = ReadData('offert.db')
    df = data_reader.query_connection()
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
                       'size': 20},
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
                       'size': 20},
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

@app.callback(Output('line_chart', 'figure'),
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
            # go.Scatter(
            #     x=covid_data_3['date'].tail(30),
            #     y=covid_data_3['Rolling Ave.'].tail(30),
            #     mode='lines',
            #     name='Rolling Average of the last 7 days - daily confirmed cases',
            #     line=dict(width=3, color='#FF00FF'),
            #     hoverinfo='text',
            #     hovertext=
            #     '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            #     '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Rolling Ave.'].tail(30)] + '<br>'
            #
            #
            # )
        ],

        'layout': go.Layout(
            title={'text': 'When advertisements were add: ' + (w_city),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
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
            yaxis=dict(title='<b>Number of offers</b>',
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



if __name__ == '__main__':
    app.run_server(debug=True)

