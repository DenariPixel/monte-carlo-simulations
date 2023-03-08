from dash import html, dcc
dropdowns = html.Div([
    html.Label('Stock:'),
    dcc.Dropdown(
        id="stock-dropdown",
        options=[
            {"label": "Nvdia (NVDA)", "value": "NVDA"},
            {"label": "Tesla (TSLA)", "value": "TSLA"},
            {"label": "Apple (AAPL)", "value": "AAPL"},
            {"label": "Microsoft (MSFT)", "value": "MSFT"},
            {"label": "Meta (META)", "value": "META"},
            {"label": "Amazon (AMZN)", "value": "AMZN"},
            {"label": "GameStop (GME)", "value": "GME"}
            ],
            value="TSLA"
            ),
            ])
