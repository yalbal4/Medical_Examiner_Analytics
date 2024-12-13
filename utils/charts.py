import plotly.express as px

def apply_filters(df, filters):
    """
    Filter dataframe

    Params:
    - df: input dataframe
    - filters: dictionary. keys are column names. values are the desired value(s)

    Returns:
    - filtered dataframe
    """
    for column, value in filters.items():
        if value is not None:
            if isinstance(value, list):
                df = df[df[column].isin(value)]
            else:
                df = df[df[column] == value]
        
    return df

def build_chart(chart_type, df, group_by_column, title, filters=None):
    if filters:
        df = apply_filters(df, filters)
    
    grouped_df = df.groupby(group_by_column).size()

    if chart_type == "Pie chart":
        return pie_chart(grouped_df, title)
    elif chart_type == "Bar chart":
        return bar_chart(grouped_df, title)
    else:
        return None

def pie_chart(df, title):
    return px.pie(
        names=df.index,
        values=df.values,
        title=title
    )

def bar_chart(df, title):
    if df.empty:
        return px.bar(
            title=f"No data available for selected filters",
            x=None,
            y=None
        )
    
    return px.bar(
        x=df.index,
        y=df.values,
        title=title
    )