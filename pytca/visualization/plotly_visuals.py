import plotly.graph_objects as go

def plot_interactive_candlestick(data):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title='Interactive Candlestick Chart',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.show()
