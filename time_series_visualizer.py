import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    ax = df.plot(kind='line', figsize=(20, 5), legend=False, color = "firebrick")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    fig = ax.figure
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df.reset_index()
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month_name()
    df_bar['month_int'] = df_bar['date'].dt.month
    df_bar = df_bar.drop(columns=['date'])
    df_bar = df_bar.groupby(['month_int', 'year', 'month'], as_index=False).mean()
    df_bar.rename({'year': 'Years', 'month': 'Months', 'value': 'Average Page Views'}, axis=1, inplace=True)

    # Draw bar plot
    ax = sns.catplot(x="Years", y="Average Page Views", hue="Months", kind="bar",
                     height=8, palette="tab10", legend=False, data=df_bar)
    plt.legend(loc='upper left', title='Months')
    fig = ax.figure

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box = df.reset_index()
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['Year'] = df_box['date'].dt.year
    df_box['Month'] = df_box['date'].dt.month
    df_box = df_box.sort_values(by=['Month'])
    df_box.rename({'value': 'Page Views'}, axis=1, inplace=True)
    df_box = df_box.drop(columns=['date'])
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_box.replace({'Month': month_dict}, inplace=True)
        
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2, figsize=(15, 6))
    sns.boxplot(x="Year", y="Page Views", data=df_box, ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)")
    sns.boxplot(x="Month", y="Page Views", data=df_box, ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
