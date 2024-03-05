import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar

def import_df():
    # Import df (Make sure to parse dates. Consider setting index column to 'date'.)
    df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date", sep=",")

    # Clean df
    df = df[
        (df["value"] >= df["value"].quantile(0.025)) &
        (df["value"] <= df["value"].quantile(0.975))]
    return df

df = import_df()

def draw_line_plot():
    # Draw line plot
    df = import_df().reset_index()
    df["date"] = df["date"].dt.date
    plt.plot(df["date"], df["value"], color="red", linewidth=0.5)
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    fig = plt.gcf()
    plt.close()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

draw_line_plot()

def draw_bar_plot():
    # Copy and modify df for monthly bar plot
    df = import_df()
    months = calendar.month_name[1:]
    df["months"] = pd.Categorical(values=df.index.strftime("%B"),categories=months,ordered=True)
    df_bar = pd.pivot_table(data=df, index=df.index.year, columns="months",values= "value")

    # Draw bar plot
    ax = df_bar.plot(kind = "bar", figsize=(12,12), ylabel= "Average Page Views", xlabel= "Years", rot=0)
    ax.legend(loc="upper left", bbox_to_anchor= (.01, 1.))

    fig = plt.gcf()
    plt.close()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

draw_bar_plot()


def draw_box_plot():
    # Prepare df for box plots (this part is done!)
    df = import_df()
    df_co = df.copy()
    df_co.reset_index(inplace=True)
    df_box = df_co.rename({"value":"Page Views"}, axis=1)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(18,10))

    sns.boxplot(ax=axes[0], data= df_box, x="Year", y="Page Views", palette="deep")
    sns.boxplot(ax=axes[1], data= df_box, x="Month", y="Page Views", palette="pastel", order=["Jan", "Feb","Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],["Jan", "Feb","Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    # df_box.sort_values(by=["month"],ascending=[True],inplace=True)
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")

    fig = plt.gcf()
    plt.close()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_box_plot()
