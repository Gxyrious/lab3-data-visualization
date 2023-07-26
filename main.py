import pandas as pd
import numpy as np
import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
import plotly.graph_objs as go

app = dash.Dash()
server = app.server
# 数据载入
df = pd.read_csv('dataset/google-play-store-apps/googleplaystore.csv', encoding='ISO-8859-1')

df = df.dropna(subset=['Rating']) # 删去评分为NaN的行
df = df[pd.to_numeric(df['Rating'], errors='coerce').between(0, 5)] # 删去评分不在0-5之间的行

def getPieChart():
    cnts = df['Category'].value_counts()
    return dict(
        data=[go.Pie(
            labels=cnts.index,
            values=cnts.values,
            hole=0.4)],
        layout=go.Layout(
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',
            margin=dict(l=50, r=50, t=50, b=50))
    )

def getScatterChart():
    return dict(
        data=[go.Scatter(
            x=df[df['Category'] == i]['Rating'],
            y=df[df['Category'] == i]['Reviews'],
            text=df[df['Category'] == i]['App'],
            name=i,
            mode='markers',
            marker=dict(
                size=10,
                color=np.random.randn(400),
                colorscale='Viridis',
                line=dict(width=1, color='white')
            ),
            hovertemplate=
                '<b>%{text}</b><br>' +
                'Rating: %{x}<br>' +
                'Reviews: %{y}<br>' +
                '<extra></extra>'
        ) for i in df.Category.unique()],
        layout=go.Layout(
            xaxis=dict(
                title='Rating',
                tickmode='linear',
                tick0=0,
                dtick=0.5,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Reviews',
                gridcolor='lightgray'
            ),
            hovermode='closest',
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',
            font=dict(family='Arial', color='black'),
            margin=dict(l=80, r=80, t=80, b=80, pad=4)
        )
    )

def getBoxPlotChart():
    return dict(
        data=[go.Box(
            y=df[df['Category'] == i]['Rating'],
            name=i,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(
                color='rgb(93, 164, 214)'
            ),
            line=dict(
                color='rgb(8, 48, 107)',
                width=1
            ),
            fillcolor='rgba(0,0,0,0)'
        ) for i in df.Category.unique()],
        layout=go.Layout(
            xaxis=dict(title='Category'),
            yaxis=dict(title='Rating'),
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',
            font=dict(family='Arial', color='black'),
            margin=dict(l=40, r=40, t=40, b=130, pad=4)
    ))

def getScatter3dChart():
    return dict(
        data=[go.Scatter3d(
            x=df[df['Category'] == i]['Size'],
            y=df[df['Category'] == i]['Rating'],
            z=df[df['Category'] == i]['Reviews'],
            text=df[df['Category'] == i]['App'],
            name=i,
            mode='markers',
            opacity=0.8,
            marker=dict(
                size=3,
                color=np.random.randn(400),
                colorscale='Viridis',
                line=dict(width=0.5, color='white')
            )
        ) for i in df['Category'].unique()],
        layout=go.Layout(
            margin=dict(l=40, b=40, t=40, r=40),
            hovermode='closest',
            scene=dict(
                xaxis=dict(title='Size'),
                yaxis=dict(title='Rating'),
                zaxis=dict(title='Reviews')
            ),
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='#f7f7f7',
            font=dict(family='Arial', color='black')
    ))


# app的layout
app.layout = html.Div([
    html.H1(id="h1-element", className='h1', children='Lab3: Data Visualization',
            style={'textAlign': 'center', 'color': '#000000','backgroundColor':'#ffffff'}),
    html.H2(id="h2-element", className='h2', children='——google play store apps',
            style={'textAlign': 'center', 'color': '#000000','backgroundColor':'#ffffff'}),
    html.Hr(style={'margin': 50, 'backgroundColor': '#ffffff'}),
    
    # figure 1
    html.Div([
        html.H3(children='App Categories Proportion', style={'textAlign': 'center', 'color': '#000000'}),
        dcc.Graph(
            id='fig1',
            figure=getPieChart()
        ),
    ], style={
        'margin': 50,
        'height': 500,
    }),

    html.Div([
        html.Div(children="We observe a clear difference in the number of apps in different categories. The top three categories are family, game and tools, which indicates that family-related apps are popular in contemporary society, game-related games are more popular among young people, and tools apps are also a necessity in People's Daily life.",
                 style={'color': '#000000','font-size':18}),
    ], style={
        'margin-left': 50,
        'margin-right': 50,
    }),
    
    html.Hr(style={'margin': 50, 'backgroundColor': '#ffffff'}),
    
    # figure 2
    html.Div([
        html.H3(children='App Ratings and Reviews', style={'textAlign': 'center', 'color': '#000000'}),
        dcc.Graph(
            id='fig2',
            figure=getScatterChart()
        ),
    ], style={
        'margin': 50,
        'height': 500,
    }),

    html.Div([
        html.Div(children="Based on the provided table, a clear correlation can be observed between the app rating and the number of reviews.  It is evident that higher ratings are associated with a greater number of reviews.  Notably, apps with ratings ranging from 3.7 to 4.8 exhibit the highest number of reviews.  The statistical findings identify Facebook, WhatsApp Messenger, and Instagram as the top three apps with the highest review counts.  Additionally, it is apparent that social and communication apps significantly outperform others in terms of the number of comments.  This suggests that, in today's digital age, the majority of social interactions occur through network-enabled devices.",
                 style={'color': '#000000','font-size':18}),
    ], style={
        'margin-left': 50,
        'margin-right': 50,
    }),
    
    html.Hr(style={'margin': 50, 'backgroundColor': '#ffffff'}),
    
    # figure 3
    html.Div([
        html.H3(children='Distribution of app ratings across categories', style={'textAlign': 'center', 'color': '#000000'}),
        dcc.Graph(
            id='fig3',
            figure=getBoxPlotChart()
        ),
    ], style={
        'margin': 50,
        'height': 500,
    }),
    
    html.Div([
        html.Div(children="Through the analysis of box plots, we find that most apps have a rating above 4, many apps have a maximum rating of 5, and values below 3 are identified as outliers because there are very few of them compared to those above 4. It can be seen that apps listed on Google are of good quality.",
                 style={'color': '#000000', 'font-size': 18}),
    ], style={
        'margin-left': 50,
        'margin-right': 50,
    }),
    
    html.Hr(style={'margin': 50, 'backgroundColor': '#ffffff'}),
    
    # figure 4
    html.Div([
        html.H3(children='3D analysis of app size, app score, number of reviews', style={'textAlign': 'center', 'color': '#000000'}),
        dcc.Graph(
            id='fig4',
            figure=getScatter3dChart()
        ),
    ], style={
        'margin': 50,
        'height': 500,
    }),
    
    html.Div([
        html.Div(children="From this figure, we can find that the rating level is often positively correlated with the number of reviews, because only when an app has high quality will more users be attracted to use it, and they will review it after using it for a period of time. At the same time, these apps with high ratings and a large number of reviews tend to have larger app size, we can simply think that more complex apps can have higher quality.",
                 style={'color': '#000000', 'font-size': 18}),
    ], style={
        'margin-left': 50,
        'margin-right': 50,
    }),
    
    

], className="page", style = dict(backgroundColor = '#ffffff'))


# css的设置
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://codepen.io/ffzs/pen/mjjXGM.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()
