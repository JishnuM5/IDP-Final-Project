'''
Create amazing plots in this file. You will read the data from `data_organized`
(unless your raw data required no reduction, in which case you can read your data from `raw_data`).
You will do plot-related work such as joins, column filtering, pivots,
small calculations and other simple organizational work.
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_dfs():
    '''
    This method creates all the DataFrames that will be used for analysis
    '''
    nsch_dfs = {}
    hbsc_dfs = {}

    # for i in range(2016, 2024):
    #     file_name = f"nsch_{i}e_topical.csv"
    #     nsch_dfs[i] = pd.read_csv("data_organized/" + file_name)
    for i in range(2002, 2019, 4):
        file_name = f"HBSC{i}.csv"
        hbsc_dfs[i] = pd.read_csv("data_organized/" + file_name)

    return (nsch_dfs, hbsc_dfs)


def filter_concat_dfs(dfs, filter_cols, exlude_dfs=None):
    # To avoid changing the original DataFrames
    plot_dfs = dfs.copy()

    if exlude_dfs is not None:
        for df_name in exlude_dfs:
            del plot_dfs[df_name]

    for year in plot_dfs:
        plot_dfs[year] = plot_dfs[year][filter_cols]
    return pd.concat(plot_dfs).dropna()


def friendship_vs_screen_time(nsch_dfs):
    def categorize_screen_time(hours):
        if hours <= 1:
            return "0-1"
        if 2 <= hours <= 3:
            return "2-3"
        else:
            return "4+"

    plot_df = filter_concat_dfs(nsch_dfs, ["Screen_Time_Total", "Difficulty_Making_Friends"])
    plot_df["Screen Time (Hours)"] = plot_df["Screen_Time_Total"].apply(categorize_screen_time)
    plot_df["Screen Time (Hours)"] = pd.Categorical(
        plot_df["Screen Time (Hours)"], ["0-1", "2-3", "4+"]
    )

    sns.histplot(
        data=plot_df, x="Screen Time (Hours)", hue="Difficulty_Making_Friends", 
        multiple="fill", stat="proportion", discrete=True, shrink=0.9
    )
    plt.gcf().set_size_inches(6, 8)
    plt.legend(loc="upper right", title="Difficulty Making Friends", labels=["A lot", "A little", "None"])
    plt.title("How Making Friends Varies with Screen Time")
    plt.savefig("plots/friends.png")


def deep_talk_vs_screen_time(nsch_dfs):
    plot_df = filter_concat_dfs(
        nsch_dfs, ["Screen_Time_Total", "Good_Communication_With_Child"], [2000 + i for i in range(18, 24)])

    GCWC_map = {
        1: "Very well",
        2: "Somewhat well",
        3: "Not very well",
        4: "Not well at all"
    }
    plot_df["Good_Communication_With_Child"] = plot_df["Good_Communication_With_Child"].map(GCWC_map)

    sns.catplot(data=plot_df, x="Screen_Time_Total", y="Good_Communication_With_Child", kind="violin")
    plt.gcf().set_size_inches(8, 4)
    plt.title("How Screen Time Varies with Depth of Relations")
    plt.xlabel("Child's Screen Time (Hours)")
    # Note in report and presentation that this is discussing with parents
    plt.ylabel("How Well Child Discusses Topics That Matter")
    plt.savefig("plots/deep_talk.png", bbox_inches='tight')


def health_screen_time_age(nsch_dfs, exclude_dfs, name):
    plot_df = filter_concat_dfs(
        nsch_dfs, ["Received_Mental_Health_Treatment", "Screen_Time_Total", "Child_Age_Years"], exclude_dfs)

    # Those who received or need mental health treatment are having a mental health condition
    plot_df["Needs Mental Health Treatment"] = plot_df["Received_Mental_Health_Treatment"].apply(
        lambda val: "No" if val == 3 else "Yes")
    # The age variable is categorized
    plot_df["Age (Years)"] = pd.cut(
        plot_df['Child_Age_Years'], 
        bins=[0, 1, 3, 5, 7, 9, 11, 13, 15, 17],
        labels=["0-1", "2-3", "4-5", "6-7", "8-9", "10-11", "12-13", "14-15", "16-17"],
        include_lowest=True,
    )
    # Finding the average screen time by age and condition
    plot_df = plot_df.groupby(["Age (Years)", "Needs Mental Health Treatment"])[
        "Screen_Time_Total"].mean().reset_index(name="Average Screen Time (Hours)")

    sns.barplot(data=plot_df, x='Average Screen Time (Hours)', y='Age (Years)',
                hue='Needs Mental Health Treatment', orient='horizontal', 
                dodge=True)
    plt.gcf().set_size_inches(8, 5)
    plt.title(f"The Screen Time Age Distribution and Mental Health, {name}")
    plt.savefig(f"plots/pop_pyr_{name}.png", bbox_inches="tight")


def life_sat_screen_time_buffers(hbsc_dfs):
    freq_6mo_map = {
        7: "About every day",
        2.5: "More than once/week",
        1: "About every week",
        0.25: "About every month",
        0: "Rarely or never"
    }

    buffers_catalysts = {
        ("self_perceived_family_wealth", "Family is Perceived To Be:", "well_off"): {
            1: "Very well off",
            2: "Quite well off",
            3: "Average",
            4: "Not very well off",
            5: "Not at all well off"
        },
        ("active_days_past_week", "Days Active in Past Week", "active"): {
            0: "0 days",
            1: "1 day",
            2: "2 days",
            3: "3 days",
            4: "4 days",
            5: "5 days",
            6: "6 days",
            7: "7 days"
        },
        ("talk_to_best_friend_difficulty", "Talking to Best Friend About Bothers Is:", "best_friend"):
        {
            1: "Very easy",
            2: "Easy",
            3: "Difficult",
            4: "Very difficult",
            5: "Don't have/see them"
        },
        ("sleep_issues_frequency_6mo", "Sleep Issues in Past 6 Months", "bad_sleep"): freq_6mo_map,
        ("headache_frequency_6mo", "Headaches in Past 6 Months", "headaches"): freq_6mo_map,
        ("irritable_frequency_6mo", "Irritability in Past 6 Months", "irritable"): freq_6mo_map,

    }

    for key in buffers_catalysts:
        hue_col, hue_title, file_name = key
        plot_df = filter_concat_dfs(
            hbsc_dfs, 
            ["computer_use_hours_weekdays", "life_satisfaction_score", hue_col], 
            [2014, 2018] if (file_name == "best_friend") else [2018]
        )
        plot_df[hue_col] = plot_df[hue_col].map(buffers_catalysts[key])
        cat_order = list(buffers_catalysts[key].values())
        plot_df[hue_col] = pd.Categorical(plot_df[hue_col], categories=cat_order, ordered=True)

        # WARNING: calculating a confidence interval is computationally heavy.
        # It increases plotting time from seconds to minutes.
        # Set `ci_val` to None (removes confidence interval) for quicker plotting.
        ci_val = 95
        sns.lmplot(data=plot_df, x="computer_use_hours_weekdays", y="life_satisfaction_score", 
                   hue=hue_col, scatter=False, legend=False, ci=ci_val)
        plt.legend(title=hue_title, loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=2)
        plt.savefig(f"plots/buffer_{file_name}.png", bbox_inches="tight")
        plt.xlabel("Daily Computer Use, Weekdays (Hours)")
        plt.ylabel("Life Satisfaction Score")
        plt.clf()


def main():
    nsch_dfs, hbsc_dfs = create_dfs()
    # friendship_vs_screen_time(nsch_dfs)
    # plt.clf()
    # deep_talk_vs_screen_time(nsch_dfs)
    # plt.clf()
    # health_screen_time_age(nsch_dfs, [2000 + i for i in range(18, 24)], "2016-2017")
    # plt.clf()
    # health_screen_time_age(nsch_dfs, [2016, 2017], "2018-2023")
    # plt.clf()
    life_sat_screen_time_buffers(hbsc_dfs)


if __name__ == "__main__":
    main()
