import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df = df.set_index("date")
month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
month_order_3char = [month[:3] for month in month_order]
# Clean data
df = df[
    (df["value"] > df["value"].quantile(0.025))
    & (df["value"] < df["value"].quantile(0.975))
]
df.index = pd.to_datetime(df.index)


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20, 6))
    plt.plot(df.index, df["value"], color="r")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", color="black")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()
    # Draw bar plot
    fig = df_bar.plot(kind="bar", legend=True, figsize=(15, 10)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    # Save image and return fig (don't change this part)
    # plt auto rotate 90 degree so we dont need to change
    # plt.xticks(rotation=30)
    # plt.xticks(fontsize = 10)
    # plt.yticks(fontsize = 10)

    plt.legend(
        # fontsize=10,
        title="Months",
        labels=month_order,
    )
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axarr = plt.subplots(1, 2, figsize=(18, 6))
    sns.boxplot(ax=axarr[0], x="year", y="value", data=df_box)
    sns.boxplot(
        ax=axarr[1], x="month", y="value", data=df_box, order=month_order_3char
    ).set(
        xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)"
    )
    axarr[0].set_title("Year-wise Box Plot (Trend)")
    axarr[0].set_xlabel("Year")
    axarr[0].set_ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
