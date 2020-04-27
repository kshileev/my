def simple():
    import plotly.express as px

    df = px.data.wind()
    fig = px.scatter_polar(df, r='frequency', theta='direction', title='Wind')
    fig.add_box()
    fig.show()


if __name__ == '__main__':
    simple()
