import plotly.express as px
import pandas as pd

# ---------------- Line Chart ----------------
def line_sales_trend(df, date_col, sales_col):
    """
    Create a line chart showing sales trend over time.
    """
    trend = df.groupby(date_col)[sales_col].sum().reset_index()
    fig = px.line(trend, x=date_col, y=sales_col, title="Sales Trend")
    fig.update_layout(xaxis_title=date_col, yaxis_title=sales_col)
    return fig

# ---------------- Bar Chart ----------------
def bar_top(df, group_col, value_col, title="Top 10"):
    """
    Create a bar chart for top N categories by value.
    """
    agg = df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(agg, x=group_col, y=value_col, title=title, text=value_col)
    fig.update_layout(xaxis_title=group_col, yaxis_title=value_col)
    return fig

# ---------------- Heatmap ----------------
def heatmap(df, x_col, y_col, value_col, title="Heatmap"):
    """
    Create a heatmap for aggregated values.
    """
    pivot_df = df.pivot_table(index=y_col, columns=x_col, values=value_col, aggfunc="sum", fill_value=0)
    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color=value_col),
        text_auto=True,
        aspect="auto",
        title=title,
        color_continuous_scale="Viridis"
    )
    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)
    return fig

# ---------------- KPI Cards ----------------
def kpi_card(value, name, color="green"):
    """
    Return a simple KPI dict to render as card in Streamlit.
    Color options: green, red, orange
    """
    return {
        "value": value,
        "name": name,
        "color": color
    }

# ---------------- Scatter Plot ----------------
def scatter_price_qty(df, price_col, qty_col, title="Price vs Quantity"):
    """
    Scatter plot of price vs quantity
    """
    fig = px.scatter(df, x=price_col, y=qty_col, title=title, hover_data=df.columns)
    fig.update_layout(xaxis_title=price_col, yaxis_title=qty_col)
    return fig

# ---------------- Pie Chart ----------------
def pie_chart(df, names_col, values_col, title="Pie Chart"):
    """
    Create a pie chart showing share of categories.
    """
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    return fig
