import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Sample dataset for the dashboard
data = {
    'Country': ['USA', 'England', 'France', 'Germany', 'Spain', 'Italy', 'Brazil', 'Argentina', 'Netherlands', 'Portugal'],
    'Wins': [20, 25, 22, 18, 24, 15, 19, 21, 16, 17],
    'Losses': [5, 3, 4, 6, 2, 5, 4, 3, 6, 5],
    'Draws': [5, 2, 3, 3, 4, 5, 3, 2, 3, 2],
    'Goals': [15, 22, 18, 10, 20, 17, 19, 21, 16, 14],
    'Latitude': [37.1, 51.5, 46.6, 51.1, 40.4, 41.9, -14.2, -38.4, 52.4, 39.6],
    'Longitude': [-95.7, -0.1, 1.4, 10.4, -3.7, 12.6, -51.9, -63.4, 5.5, -8.4],
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout with responsive design
app.layout = html.Div(style={'backgroundColor': '#2c3e50', 'color': 'white', 'height': '100vh', 'margin': '0'}, children=[
    html.H1("Sports Statistics Dashboard", style={'text-align': 'center', 'margin-bottom': '20px'}),
    
    dcc.Dropdown(id='country-dropdown', 
                 options=[{'label': country, 'value': country} for country in df['Country']],
                 value='USA', multi=False, style={'width': '50%', 'margin': 'auto', 'color': 'black'}),
    
    html.Div(id='data-summary', style={'text-align': 'center', 'margin': '20px', 'font-size': '18px'}),
    
    html.Div(style={'display': 'flex', 'flex-direction': 'row', 'height': '65vh'}, children=[
        dcc.Graph(id='world-map', style={'width': '50%', 'height': '100%'}),
        html.Div(style={'width': '50%', 'padding': '20px', 'display': 'flex', 'flex-direction': 'column'}, children=[
            dcc.Graph(id='performance-pie', style={'height': '50%', 'margin-bottom': '20px'}),
            html.Div(style={'display': 'flex', 'justify-content': 'space-around', 'height': '50%'}, children=[
                dcc.Graph(id='wins-bar', style={'width': '48%', 'height': '100%', 'margin': '0'}),
                dcc.Graph(id='losses-bar', style={'width': '48%', 'height': '100%', 'margin': '0'}),
            ])
        ]),
    ]),
    
    html.Div(style={'margin-top': '20px'}, children=[
        dcc.Graph(id='draws-bar', style={'width': '100%', 'height': '50vh'}),
    ])
])

# Callbacks for interactivity
@app.callback(
    Output('data-summary', 'children'),
    Output('world-map', 'figure'),
    Output('performance-pie', 'figure'),
    Output('wins-bar', 'figure'),
    Output('losses-bar', 'figure'),
    Output('draws-bar', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graphs(selected_country):
    filtered_df = df[df['Country'] == selected_country]
    
    # Data Summary
    summary = f"Wins: {filtered_df['Wins'].values[0]}, Losses: {filtered_df['Losses'].values[0]}, Draws: {filtered_df['Draws'].values[0]}"

    # World Map
    map_fig = go.Figure(data=go.Scattergeo(
        lon=filtered_df['Longitude'],
        lat=filtered_df['Latitude'],
        text=selected_country,
        marker=dict(size=10, color='blue', opacity=0.8),
    ))
    map_fig.update_layout(
        geo=dict(
            scope='world',
            projection_type='orthographic',
            showland=True,
            landcolor='lightgreen',
            countrycolor='lightgrey',
            bgcolor='rgba(0,0,0,0)',  # Transparent background
        ),
        title=f"{selected_country} Location",
        title_x=0.5,
        paper_bgcolor='#2c3e50',
        plot_bgcolor='#2c3e50',
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    

    # Pie Chart
    performance_pie = px.pie(names=['Wins', 'Losses', 'Draws'],
                              values=[filtered_df['Wins'].values[0], 
                                      filtered_df['Losses'].values[0], 
                                      filtered_df['Draws'].values[0]],
                              title=f'Performance of {selected_country}')
    performance_pie.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

    # Wins Bar Chart
    wins_bar = px.bar(df, x='Country', y='Wins', title='Wins by Country', color='Wins', color_continuous_scale=px.colors.sequential.Blues)
    wins_bar.update_layout(yaxis_title='Wins', paper_bgcolor='black', plot_bgcolor='black', font_color='white', showlegend=False)

    # Losses Bar Chart
    losses_bar = px.bar(df, x='Country', y='Losses', title='Losses by Country', color='Losses', color_continuous_scale=px.colors.sequential.Reds)
    losses_bar.update_layout(yaxis_title='Losses', paper_bgcolor='black', plot_bgcolor='black', font_color='white', showlegend=False)

    # Draws Bar Chart
    draws_bar = px.bar(df, x='Country', y='Draws', title='Draws by Country', color='Draws', color_continuous_scale=px.colors.sequential.Greens)
    draws_bar.update_layout(yaxis_title='Draws', paper_bgcolor='black', plot_bgcolor='black', font_color='white', showlegend=False)

    return summary, map_fig, performance_pie, wins_bar, losses_bar, draws_bar

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
