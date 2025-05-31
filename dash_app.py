from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Below are columns from HBSC datasets that we define as indicators of health
# We chose variables that we felt could either relate to screen time or mental health
health_cols = ["fruit_intake_weekly", "vegetable_intake_weekly", "sweets_intake_weekly", 
               "soft_drink_intake_weekly", "active_days_past_week", "active_days_usual_week",
               "exercise_hours_weekly", "headache_frequency_6mo", "backache_frequency_6mo", 
               "feel_low_frequency_6mo", "irritable_frequency_6mo", "nervous_frequency_6mo",
               "sleep_issues_frequency_6mo", "life_satisfaction_score", "bullied_frequency_recent",
               "bullying_others_frequency", "fights_past_year", "dinners_with_parents_frequency",
               "homework_hours_weekdays", "homework_hours_weekends", "bullied_through_messages_frequency",
               "bullied_through_pictures_frequency", "family_support_score", "family_talk_score",
               "friend_help_score", "family_help_score", "friend_share_score", "friend_talk_score",
               "exercise_days_weekly"
               ]

# Below are columns from HBSC datasets that we define as indicators of screen time
screen_cols = ["tv_hours_weekdays", "tv_hours_weekends", "video_game_hours_weekdays", 
               "video_game_hours_weekends", "computer_use_hours_weekdays", "computer_use_hours_weekends",
               "e_communication_frequency_weekly", "family_computer_count", "online_freq_close_friends",
               "online_freq_friends", "online_freq_online_friends", "online_freq_other", 
               "talk_to_friends_phone_internet_freq", "talk_to_friends_text_freq",
               "talk_to_friends_email_freq", "talk_to_friends_social_media_freq"
               ]
# All DataFrames to be used are created here
years = [2002, 2006, 2010, 2014, 2018]
dfs = {}
for year in years:
    dfs[year] = pd.read_csv(f'data_organized/HBSC{year}.csv')


def get_present_cols(df, all_cols):
    '''
    This method returns all columns from a given list that are present in a DataFrame
    '''
    return [col for col in all_cols if col in df.columns]


# 2002 is the default year
present_health_cols = get_present_cols(dfs[2002], health_cols)
present_screen_cols = get_present_cols(dfs[2002], screen_cols)

# This is the primary layout of the app, using html-style components,
# along with some bootstrap formatting and layout components
app.layout = dbc.Container([
    html.H1('Screen Time & Mental Health in European Adolescents', className='mb-4 mt-2 text-center'),
    # Below are the dropdowns to select variables
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='health-dropdown',
                options=[{'label': col, 'value': col} for col in present_health_cols],
                value=present_health_cols[0],
                clearable=False,
                style={'width': '80%', 'display': 'inline-block'}
            ), 
            width=6,
            style={'textAlign': 'center'},
        ),
        dbc.Col(
            dcc.Dropdown(
                id='screen-dropdown',
                options=[{'label': col, 'value': col} for col in present_screen_cols],
                value=present_screen_cols[0],
                clearable=False,
                style={'width': '80%', 'display': 'inline-block', }
            ), 
            width=6,
            style={'textAlign': 'center'},
        ),
    ], className='mb-4'),

    # Below is the slider to set the year of data to look at
    html.Div(
        html.Div(
            dcc.Slider(
                2002, 2018, 4, 
                id='year-slider', 
                marks={year: str(year) for year in years}, 
                value=2002,
                className='mb-4',
            ),
            style={'width': '50%'},
        ),
        style={
            'display': 'flex',
            'justifyContent': 'center',
        }
    ),

    # Here is the choropleth graph itself
    html.Div(
        dcc.Graph(id='corr_choropleth', style={'width': '100%', 'height': '70vh'}),
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'width': '100%',
        }
    ),
], fluid=True)


# Callback methods ensure the method runs and an output value is given every time some input(s) change
@callback(
    Output('health-dropdown', 'options'),
    Output('health-dropdown', 'value'),
    Output('screen-dropdown', 'options'),
    Output('screen-dropdown', 'value'),
    Input('year-slider', 'value'),
)
def update_dropdowns(year):
    '''
    This method updates the dropdown's list's values when the slider changes,
    as the variables available to correlate can change year-by-year
    '''
    df = dfs[year]
    health = get_present_cols(df, health_cols)
    screen = get_present_cols(df, screen_cols)
    health_options = [{'label': col, 'value': col} for col in health]
    screen_options = [{'label': col, 'value': col} for col in screen]
    return (health_options, health[0], screen_options, screen[0])


@callback(
    Output('corr_choropleth', 'figure'),
    Input('health-dropdown', 'value'),
    Input('screen-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_choropleth(health_col, screen_col, year):
    '''
    This method updates the graph based on chosen dropdown and year variables.
    '''
    # Calculate correlation for each country
    corr_df = dfs[year][[health_col, screen_col, "ISO_code"]].dropna()
    corr_df = corr_df.groupby('ISO_code') \
        .apply(lambda grp: grp[health_col].corr(grp[screen_col]), include_groups=False) \
        .reset_index(name='correlation')

    # Create the actual choropleth map
    fig = px.choropleth(
        corr_df,
        locations="ISO_code",
        color="correlation",
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        title=f'Pearson Correlation between {health_col} and {screen_col} by Country'
    )
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_geos(landcolor="LightGrey")
    return fig


if __name__ == '__main__':
    app.run(debug=True)