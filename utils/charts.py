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

def pie_chart(df, group_by_column, title, filters=None):
    if filters:
        df = apply_filters(df, filters)
    
    grouped_df = df.groupby(group_by_column).size()
    return px.pie(
        names=grouped_df.index,
        values=grouped_df.values,
        title=title
    )

def bar_chart(df, group_by_column, title, filters=None):
    if filters:
        df = apply_filters(df, filters)

    grouped_df = df.groupby(group_by_column).size()
    return px.bar(
        names=grouped_df.index,
        values=grouped_df.values,
        title=title
    )