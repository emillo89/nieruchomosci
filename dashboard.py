import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from connect_with_database import DatabaseConnect
from readDatabase import ReadData



df = ReadData('offert.db')
con = df.query_connection()

'''1. How many add in database'''
total_count = df.count_totat_add()

'''2. Kind of investments'''
houses = df.count_houses()
flats = df.count_flats()
print(houses)






app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('analytics.png'),
                     id='logo-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'}

            )
        ], className='one-third column'),

        html.Div([
            html.Div([
                html.H3('Data analysis flats and houses', style={'margin-bottom':'0px', 'color':'white'})

            ])

        ], className='one-half column', id='title'),


    ], id='header', className='row flex-display', style={'margin-buttom':'25px'}),


    html.Div([
           html.Div([
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

            html.Div([
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': '#dd1e35',
                               'fontSize': 40}),
           ], className='card_container three columns'),


            html.Div([
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': 'green',
                               'fontSize': 40}),
           ], className='card_container three columns'),

            html.Div([
                html.H6(children='....',
                        style={'textAlign': 'center',
                               'color': 'white'
                               }),
                html.P(f'{total_count}',
                        style={'textAlign': 'center',
                               'color': '#e55467',
                               'fontSize': 40}),
           ], className='card_container three columns')

    ], className='row flex display'),


    html.Div([
        html.Div([
            html.P('Select city:', className='fix_label',style={'color':'white'}),
            dcc.Dropdown

        ], className='create_container three columns')

    ], className='row flex-display')




], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'} )



if __name__ == '__main__':
    app.run_server(debug=True)


# '''1.How many offers per a city'''
# flats_per_city = df.groupby(['city'], as_index=False).agg({'id':pd.Series.count}).sort_values('id', ascending=False)
#
# '''2. What is average per 1m2 in city'''
# price_per_1m2 = (df.price // df.area).apply(np.ceil)
# df.insert(5,'price_per_1m2', price_per_1m2)
#
# '''3. Average price per 1m2'''
# city_average_price_per_1m = (df.groupby(['city']).agg({'price_per_1m2': pd.Series.mean})).round(0).sort_values(by='price_per_1m2', ascending=False)
# city_average_price_per_1m=city_average_price_per_1m.sort_values(by='price_per_1m2', ascending=False)
#
# fig = px.bar(city_average_price_per_1m,
#              x=city_average_price_per_1m.index,
#              y=city_average_price_per_1m.price_per_1m2,
#              color=city_average_price_per_1m.price_per_1m2,
#              color_continuous_scale='Emrld')
# fig.update_layout(title={
#     'text': "Average price for 1m2",
#     'y': 0.95,
#     'x': 0.5,
#     'xanchor': 'center',
#     'yanchor': 'top'},
#     xaxis_title="City",
#     yaxis_title="price",
#     legend_title=" ",
#     font=dict(
#         family="Courier New, monospace",
#         size=14,
#         color="black"
#     ))
#
# fig.show()
#
# '''4. Area ranges per city and count their number'''
# df.insert(6, 'mean_area','Unkown')
# df.mean_area = ['<39' if i < 39 else '40-59' if i < 60 else '60-79' if i <80 else '>79' for i in df.area]
# area_range = df.groupby(['city', 'mean_area',],as_index=False).agg({'area': pd.Series.count}).sort_values(by=['area','city'], ascending=False)
#
# fig = px.pie(area_range, values=area_range.area, names=area_range.mean_area, hole=.5)
# fig.show()
#
# '''5 Count offert per primary and secondary market'''
# market_kind = df.groupby(['city', 'market'],as_index=False).agg({'area': pd.Series.count}).sort_values(by=['area','city'], ascending=False)
#
# fig = px.pie(market_kind, values=market_kind.area, names=market_kind.market, hole=.5)
#
# fig.update_traces(textinfo='percent + label')
# fig.show()

# app = Dash(__name__)
#
# fig = px.bar(x=city_average_price_per_1m.index,
#              y=city_average_price_per_1m.price_per_1m2,
#              color=city_average_price_per_1m.index)
#
# app.layout = html.Div(children=[html.H1(children='Hello Dash'),
#                                 html.Div(children='''
#                                 Dash: A web application'''),
#
#                                 dcc.Graph(
#                                     id='example-graph',
#                                     figure=fig
#                                 )])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)


