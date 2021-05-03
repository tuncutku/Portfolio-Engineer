import pandas as pd
import plotly.express as px  # (version 4.7.0)
from datetime import datetime as dt
from flask import redirect, url_for, session

from dash import Dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from src.environment.user import User
from src.environment.portfolio import Portfolio


def register_dash_app(server):
    app = Dash(
        __name__,
        server=server,
        assets_url_path="src/dashapp/assets",
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
                        html.Div(
                            [
                                dbc.Button(
                                    "View my account",
                                    id="account_btn",
                                    className="mr-2",
                                ),
                                dbc.Button("Log Out", id="logout_btn"),
                            ],
                        ),
                    ],
                    fluid=True,
                ),
                color="primary",
                className="mb-4",
            ),
            # Main
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("Choose portfolio:"),
                                    dcc.Dropdown(
                                        id="portfolios",
                                        multi=False,
                                        searchable=False,
                                        clearable=False,
                                        style={"width": "150px"},
                                    ),
                                    html.H6("Choose return period:"),
                                    dcc.Dropdown(
                                        id="period",
                                        multi=False,
                                        searchable=False,
                                        clearable=False,
                                        style={"width": "150px"},
                                        options=[
                                            {"label": "1d", "value": 1},
                                            {"label": "1w", "value": 5},
                                            {"label": "1m", "value": 22},
                                            {"label": "1y", "value": 252},
                                        ],
                                        value=1,
                                    ),
                                    html.H6("Select observation period:"),
                                    dcc.DatePickerRange(
                                        id="DateRangePickerInput",
                                        with_portal=True,
                                        number_of_months_shown=2,
                                        # display_format="MMM Do, YY"
                                        month_format="MMMM, YYYY",
                                    ),
                                ],
                                width={"size": 3},
                            ),
                            dbc.Col(
                                [],
                                width={"size": 3},
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dcc.Graph(id="cum_return_graph"),
                                    className="pretty-card",
                                ),
                                width={"size": 6},
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dcc.Graph(id="position_return_graph"),
                                    className="pretty-card",
                                ),
                                width={"size": 4},
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dcc.Graph(id="value_graph"),
                                    className="pretty-card",
                                ),
                                width={"size": 4},
                            ),
                        ]
                    ),
                ],
                fluid=True,
            ),
        ],
        className="bg-light",
    )

    # ------------------------------------------------------------------------------
    # Callbacks

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
        ],
        Input("url", "pathname"),
        prevent_initial_call=False,
    )
    def set_default_options(url):

        current_user = User.find_by_id(session["user_id"])
        primary_port = Portfolio.get_primary(current_user)

        value = primary_port.id
        options = [
            {"label": port.name, "value": port.id}
            for port in current_user.portfolios
            if port.positions
        ]

        return options, value

    @app.callback(
        [
            Output("DateRangePickerInput", "min_date_allowed"),
            Output("DateRangePickerInput", "max_date_allowed"),
            Output("DateRangePickerInput", "start_date"),
            Output("DateRangePickerInput", "end_date"),
        ],
        Input("portfolios", "value"),
    )
    def update_date_range(port_id):
        port = Portfolio.find_by_id(port_id)
        report = Report(portfolio=port)
        start, end = report.get_date_range()
        return start, end, start, end

    @app.callback(
        Output("cum_return_graph", "figure"),
        [
            Input("portfolios", "value"),
            Input("DateRangePickerInput", "start_date"),
            Input("DateRangePickerInput", "end_date"),
        ],
    )
    def update_portfolio_return_graph(port_id, start_date, end_date):

        port = Portfolio.find_by_id(port_id)
        report = Report(portfolio=port)
        fig = px.line(report.get_cum_returns(start_date, end_date))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="Historical cumulative returns",
            height=300,
            margin=dict(l=60, r=20, t=60, b=20),
        )
        return fig

    @app.callback(
        Output("value_graph", "figure"),
        [
            Input("portfolios", "value"),
            Input("DateRangePickerInput", "start_date"),
            Input("DateRangePickerInput", "end_date"),
        ],
    )
    def update_value_graph(port_id, start_date, end_date):

        port = Portfolio.find_by_id(port_id)
        report = Report(portfolio=port)
        fig = px.line(report.get_position_values(start_date, end_date))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="Position values",
            height=300,
            margin=dict(l=80, r=20, t=60, b=20),
        )

        return fig

    @app.callback(
        Output("position_return_graph", "figure"),
        [
            Input("portfolios", "value"),
            Input("period", "value"),
        ],
    )
    def update_position_return_graph(port_id, period):

        port = Portfolio.find_by_id(port_id)
        report = Report(portfolio=port)
        position_return = report.get_returns(period)
        tail = position_return.tail(1)
        date = tail.index.date[0]
        fig = px.bar(tail.T)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="Position returns as of {}".format(date.strftime(format="%d %B, %Y")),
            showlegend=False,
            height=300,
            yaxis_tickformat="%.format.%3f",
            margin=dict(l=80, r=20, t=60, b=20),
        )

        return fig