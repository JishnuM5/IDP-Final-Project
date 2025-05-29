from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

app = Dash()

health_cols = ["fruit_intake_weekly", "vegetable_intake_weekly", "sweets_intake_weekly", 
               "soft_drink_intake_weekly", "active_days_past_week", "exercise_days_weekly",
               "exercise_hours_weekly", "headache_frequency_6mo", "backache_frequency_6mo", 
               "feel_low_frequency_6mo", "irritable_frequency_6mo", "nervous_frequency_6mo",
               "sleep_issues_frequency_6mo", "life_satisfaction_score", "bullied_frequency_recent",
               "bullying_others_frequency", "fights_past_year", "dinners_with_parents_frequency",
               "homework_hours_weekdays", "homework_hours_weekends", "bullied_through_messages_frequency",
               "bullied_through_pictures_frequency", "family_support_score", "family_talk_score",
               "friend_help_score", "family_help_score", "friend_share_score", "friend_talk_score",
               "talk_to_friends_phone_internet_freq", "talk_to_friends_text_freq",
               "talk_to_friends_email_freq", "talk_to_friends_social_media_freq"
               ]

screen_cols = ["tv_hours_weekdays", "tv_hours_weekends", "video_game_hours_weekdays", 
               "video_game_hours_weekends", "computer_use_hours_weekdays", "computer_use_hours_weekends", 
               "e_communication_frequency_weekly", "family_computer_count", "online_freq_close_friends",
               "online_freq_friends", "online_freq_online_friends", "online_freq_other"
               ]
df = pd.read_csv('data_organized/HBSC2002.csv')
present_screen_cols = [col for col in screen_cols if col in df.columns]
present_health_cols = [col for col in health_cols if col in df.columns]

app.layout = html.Div([
    html.H1('Screen Time & Mental Health in European Adolescents'),
    html.Hr(),
    html.Div([
        dcc.Dropdown(
            id='health-dropdown',
            options=[{'label': col, 'value': col} for col in present_health_cols],
            value=present_health_cols[0],
            clearable=False,
            style={'width': '45%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='screen-dropdown',
            options=[{'label': col, 'value': col} for col in present_screen_cols],
            value=present_screen_cols[0],
            clearable=False,
            style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%'}
        ),
    ]),
    dcc.Graph(id='choropleth')
])


@callback(
    Output('choropleth', 'figure'),
    Input('health-dropdown', 'value'),
    Input('screen-dropdown', 'value')
)
def update_choropleth(health_col, screen_col):
    # Calculate correlation for each country
    corr_df = df[[health_col, screen_col, "ISO_code"]].dropna()

    corr_df = corr_df.groupby('ISO_code') \
        .apply(lambda grp: grp[health_col].corr(grp[screen_col]), include_groups=False) \
        .reset_index(name='correlation')
    print(corr_df)

    fig = px.choropleth(
        corr_df,
        locations="ISO_code",
        color="correlation",
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        title=f'Pearson Correlation between {health_col} and {screen_col} by Country'
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)