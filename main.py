import datetime as dt
import numpy as np
import plotly.graph_objs as go
import yfinance as yf

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from stock_selection import dropdowns

# Define the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Monte Carlo Simulation of Stock Prices"),
    html.Div([dropdowns]),
        dcc.DatePickerSingle(
            id="start-date-picker",
            min_date_allowed=dt.date(2010, 1, 1),
            max_date_allowed=dt.date.today(),
            initial_visible_month=dt.date.today(),
            date=dt.date(2023, 1, 1),
        ),
        html.Label("Number of Simulations"),
        dcc.Input(
            id="num-simulations-input",
            type="number",
            value=500,
            min=10,
            max=3000,
            step=10
        ),
        html.Div(id="output"),
    dcc.Graph(id="stock-graph")
])

# Define the callback for updating the graph
@app.callback(
    Output("stock-graph", "figure"),
    [Input("stock-dropdown", "value"),
     Input("start-date-picker", "date"),
     Input("num-simulations-input", "value")],
)
def update_graph(stock_t, start_date, num_simulations):
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    today = dt.date.today().strftime('%Y-%m-%d')

    # Define some input parameters
    ticker = yf.Ticker(stock_t)
    initial_price = ticker.history(period="1d")["Close"].iloc[-1]
    volatility = stock_volatility(stock_t, start_date, today)
    expected_return = stock_expected_return(stock_t, start_date, today)
    num_steps = 252 # Number of trading days in a year

    # Generate random numbers for the simulation
    rand = np.random.normal(size=(num_simulations, num_steps))

    # Calculate the daily returns of the stock
    daily_returns = expected_return / num_steps + volatility * np.sqrt(1 / num_steps) * rand

        # Calculate the stock prices over time
    price_matrix = np.zeros_like(rand)
    price_matrix[:, 0] = initial_price
    for i in range(1, num_steps):
        price_matrix[:, i] = price_matrix[:, i - 1] * np.exp(daily_returns[:, i])

    # Plot the results using Plotly Graph Objects
    fig = go.Figure()
    for i in range(num_simulations):
        fig.add_trace(go.Scatter(x=list(range(num_steps)), y=price_matrix[i], mode='lines', line=dict(width=0.5, color='blue'), showlegend=False))

    fig.add_shape(
        type='line',
        x0=0, y0=initial_price,
        x1=num_steps-1, y1=initial_price,
        line=dict(color='red', width=2, dash='dash'),
        xref='x', yref='y',
    )

    fig.update_layout(
        title=f"Monte Carlo simulation of {stock_t} stock price",
        xaxis_title='Time (days)',
        yaxis_title='Stock price',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        xaxis=dict(showline=True, linecolor='black', mirror=True),
        yaxis=dict(showline=True, linecolor='black', mirror=True),
    )

    return fig

def stock_volatility(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    log_returns = np.log(stock_data['Adj Close'] / stock_data['Adj Close'].shift(1))
    volatility = log_returns.std() * np.sqrt(252)
    return volatility

def stock_expected_return(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    log_returns = np.log(stock_data['Adj Close'] / stock_data['Adj Close'].shift(1))
    expected_return = log_returns.mean() * 252
    return expected_return

if __name__ == '__main__':
    app.run_server()