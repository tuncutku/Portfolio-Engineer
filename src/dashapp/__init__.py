import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from flask import redirect, url_for, session

from dash import Dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.report import Report


def register_dash_app(server):
    app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/report/",
        external_stylesheets=[dbc.themes.FLATLY],
    )

    # ------------------------------------------------------------------------------
    # App layout
    app.layout = html.Div(
        [
            # Hidden Items
            dcc.Location(id="url", refresh=False),
            html.Div(id="hidden_log_out"),
            html.Div(id="hidden_account_view"),
            # Navbar
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.NavbarBrand(
                            children="Portfolio Engineer", className="text-light"
                        ),
                        dbc.Button("View my account", id="account_btn"),
                        dbc.Button("Log Out", id="logout_btn"),
                    ],
                    fluid=True,
                ),
                color="success",
            ),
            html.Br(),
            # Main
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="portfolios",
                                    multi=False,
                                    searchable=False,
                                    clearable=False,
                                ),
                            ],
                        ),
                        dbc.Col(dcc.Graph(id="return_graph"), width={"size": 8}),
                    ]
                ),
                fluid=True,
            ),
        ]
    )

    @app.callback(
        Output("hidden_log_out", "children"),
        [Input("logout_btn", "n_clicks")],
    )
    def logout(n):
        if n is not None:
            return dcc.Location(pathname="/users/logout", id="heey")

    @app.callback(
        Output("hidden_account_view", "children"),
        [Input("account_btn", "n_clicks")],
    )
    def account(n):
        if n is not None:
            return dcc.Location(pathname="/portfolio/list", id="heey")

    @app.callback(
        [
            Output("portfolios", "options"),
            Output("portfolios", "value"),
            Output("return_graph", "figure"),
        ],
        Input("url", "pathname"),
        prevent_initial_call=False,
    )
    def set_default_options(url):

        current_user = User.find_by_id(session["user_id"])
        primary_port = Portfolio.get_primary(current_user)
        report = Report(portfolio=primary_port)

        value = primary_port.id
        options = [
            {"label": port.name, "value": port.id}
            for port in current_user.portfolios
            if port.positions
        ]
        graph = px.line(report.cum_return)

        return options, value, graph
