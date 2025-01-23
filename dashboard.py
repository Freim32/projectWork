from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Configurazione della dashboard
data_file = "data/greenhouse_data.csv"
update_interval = 60 * 1000  # 60 secondi
variables = ["temperature", "humidity", "light", "co2", "water_usage"]

# Creazione dell'app Dash
app = Dash(__name__)


def create_value_boxes():
    """Crea i riquadri per la visualizzazione dei valori delle variabili."""
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        id=f"{var}-box",
                        style={
                            "width": "45%",
                            "display": "inline-block",
                            "padding": "15px",
                            "borderRadius": "15px",
                            "textAlign": "center",
                            "margin": "5px",
                            "border": "2px",
                        },
                    )
                    for var in variables[:2]
                ],
                style={"display": "flex", "justify-content": "center"},
            ),
            html.Div(
                [
                    html.Div(
                        id=f"{var}-box",
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "padding": "15px",
                            "borderRadius": "15px",
                            "textAlign": "center",
                            "margin": "5px",
                            "border": "2px",
                        },
                    )
                    for var in variables[2:]
                ],
                style={"display": "flex", "justify-content": "center"},
            ),
        ],
        style={"marginBottom": "20px"},
    )


def create_layout():
    """Crea il layout della dashboard."""
    return html.Div(
        [
            html.H1(
                "Dashboard Monitoraggio Serra",
                style={
                    "textAlign": "center",
                    "fontFamily": "Arial",
                    "fontWeight": "bold",
                },
            ),
            create_value_boxes(),
            html.Div(
                [
                    dcc.Dropdown(
                        id="variable-selector",
                        options=[{"label": var, "value": var} for var in variables],
                        value=["temperature", "light"],
                        multi=True,
                        style={"width": "65%"},
                    )
                ],
                style={"margin": "20px"},
            ),
            dcc.Graph(id="time-series-graph", style={"margin": "20px"}),
            dcc.Interval(id="interval-update", interval=update_interval, n_intervals=0),
        ],
        style={"fontFamily": "Arial", "backgroundColor": "#f9f9f9", "padding": "20px"},
    )


def process_data():
    """Legge e processa i dati."""
    df = pd.read_csv(data_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.tail(144)
    smoothed_df = df.copy()
    for var in variables:
        smoothed_df[var] = df[var].rolling(window=10, min_periods=1).mean()
    norm_df = smoothed_df.copy()
    for var in variables:
        norm_df[var] = (smoothed_df[var] - smoothed_df[var].min()) / (
            smoothed_df[var].max() - smoothed_df[var].min() + 1e-5
        )
    return df, smoothed_df, norm_df


@app.callback(
    [Output("time-series-graph", "figure")]
    + [Output(f"{var}-box", "children") for var in variables],
    [Input("interval-update", "n_intervals"), Input("variable-selector", "value")],
)
def update_graph(n_intervals, selected_vars):
    """Aggiorna il grafico e i valori medi e attuali."""
    df, smoothed_df, norm_df = process_data()
    fig = go.Figure()
    for var in selected_vars:
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=norm_df[var],
                mode="lines",
                name=var,
                customdata=smoothed_df[var],
                hovertemplate="%{customdata:,.2f}",
            )
        )

    fig.update_layout(
        title="Andamento Variabili",
        xaxis_title="Tempo",
        yaxis_title="Valore Normalizzato",
        template="plotly_white",
    )

    # Calcolo dei valori medi e attuali
    latest_values = df.iloc[-1]
    mean_values = df.mean()

    value_boxes = [
        html.Div(
            [
                html.H3(var.capitalize().replace("_", " "), style={"margin": "5px"}),
                html.Div(
                    [
                        html.Div(
                            "Media",
                            style={
                                "display": "inline-block",
                                "width": "50%",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            "Attuale",
                            style={
                                "display": "inline-block",
                                "width": "50%",
                                "textAlign": "center",
                            },
                        ),
                    ],
                    style={"marginBottom": "5px"},
                ),
                html.Div(
                    [
                        html.Div(
                            f"{mean_values[var]:.2f}",
                            style={
                                "display": "inline-block",
                                "width": "50%",
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                        html.Div(
                            f"{latest_values[var]:.2f}",
                            style={
                                "display": "inline-block",
                                "width": "50%",
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                    ]
                ),
            ],
            style={
                "border": "2px solid #ddd",
                "borderRadius": "15px",
                "padding": "15px",
                "margin": "5px",
                "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                "backgroundColor": "#ffffff",
            },
        )
        for var in variables
    ]

    return [fig] + value_boxes


app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
