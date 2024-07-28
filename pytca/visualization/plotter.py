import matplotlib.pyplot as plt

def plot_candlestick(data):
    fig, ax = plt.subplots()
    ax.plot(data['Date'], data['Close'], label='Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Candlestick Chart')
    plt.legend()
    plt.show()
