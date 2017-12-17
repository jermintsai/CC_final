
# coding: utf-8

# In[1]:


import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

eudata = pd.read_csv("https://raw.githubusercontent.com/jermintsai/CC_final/master/nama_10_gdp_1_Data.csv")
available_indicators = eudata['NA_ITEM'].unique()
available_countries = eudata['GEO'].unique()
print(eudata.head())


# In[ ]:


#D1
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

eudata1 = eudata[eudata['UNIT'] == 'Current prices, million euro']
app.layout = html.Div([  
    html.Div([
        
        html.Div([
            dcc.Dropdown( 

                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators]
            )
        ],
        style={'width': '60%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators]
            )
        ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
  dcc.Graph(id='Graph1'),

    
    html.Div(dcc.Slider( 
        id='year--slider',
        min=eudata['TIME'].min(),
        max=eudata['TIME'].max(),
        value=eudata['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eudata['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),
    
#D2
        html.Div([
        
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators]
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "European Union (28 countries)"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
     dcc.Graph(id='Graph2'),

])

#callback D1
@app.callback(
    dash.dependencies.Output('Graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

    eudata_year = eudata[eudata['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=eudata_year[eudata_year['NA_ITEM'] == xaxis_column_name]['Value'],
            y=eudata_year[eudata_year['NA_ITEM'] == yaxis_column_name]['Value'],
            text=eudata_year[eudata_year['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.4, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 0},
            hovermode='closest'
        )
    }

#callback D2
@app.callback(
    dash.dependencies.Output('Graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
   
    eudata_year = eudata1[eudata1['GEO'] == yaxis_column_name]


    return {
        'data': [go.Scatter(
            x=eudata_year['TIME'].unique(),
            y=eudata_year[eudata_year['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Time',
                'type': 'linear'
            },
            yaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 0},
            hovermode='closest'
        )
    }

#Running it on the server
if __name__ == '__main__':
    app.run_server()

