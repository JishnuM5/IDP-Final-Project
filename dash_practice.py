from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

app = Dash()

df = pd.read_csv('raw_data/HBSC2002OAed1.0_F4.csv')

app.layout = [
    html.Div(children='Screen Time & Mental Health in European Adolescents'),
    html.Hr(),
    # dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    # dash_table.DataTable(data=df.to_dict('records'), page_size=8),
    dcc.Graph(figure=px.choropleth(df), id='controls-and-graph')
]


# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig


if __name__ == '__main__':
    app.run(debug=True)