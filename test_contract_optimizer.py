import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import time

import datetime
import json
import pandas as pd
import numpy as np
import math

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *
from simulation_cal import *


from app import app

#app = dash.Dash(__name__, url_base_pathname='/vbc-demo/')

#server = app.server

global default_input, custom_input

df_quality = pd.read_csv("data/quality_setup.csv")
df_carve_out = pd.read_csv("data/df_carve_out.csv")
df_carve_out_details=pd.read_csv('data/df_carve_out_details.csv')


#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']


def create_layout(app):
    global default_input, custom_input
#    load_data()
    return html.Div(
                [ 
                    html.Div(load_files(), id='load-file', style = {'display':'none'}),
#                    dcc.Interval(
#                        id='interval-load-file',
#                        interval=10*1000, # in milliseconds
#                        n_intervals=0
#                    ),

                    html.Div([Header_contract(app, False, True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.A(id="top"),

                    html.Div(
                        [
                            dbc.Tabs(
                                [
                                    dbc.Tab(tab_setup(app), label="Contract Simulation Setup", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                    dbc.Tab(tab_result(app), label="Result", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                    
                                ], id = 'tab_container'
                            )
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),

                    # hidden div inside the app to store the temp data
                    html.Div(id = 'temp-data', style = {'display':'none'}),
                    html.Div(id = 'temp-result', style = {'display':'none'}),
                    html.Div(id = 'temp-carveout', style = {'display':'none'}),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )

def load_files():
    global default_input, custom_input
    file = open('configure/default_ds.json', encoding = 'utf-8')
    default_input = json.load(file)
    custom_input = json.load(open('configure/input_ds.json', encoding = 'utf-8'))

    return []

def tab_setup(app):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H1("Contract Simulation Setup", style={"padding-left":"2rem","font-size":"3"}), width=8),
                            dbc.Col(html.Div(html.H2("LOB", style={"padding":"0.5rem","color":"#F5B111", "background-color":"#ffe6ab", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                            dbc.Col(
                                dcc.Dropdown(
                                    #id = 'dropdown-firstdollar-loss', 
                                    options = [{'label': 'Medicare FFS', 'value': 1,'disabled':True}, {'label':'MA/MAPD','value' : 2}, {'label':'Commercial','value' : 3,'disabled':True}],
                                    value = 2
                                ), 
                                width = 3
                            ),
                        ],
                        style={"padding-top":"2rem"}
                    ),
                    # html.Div(
     #                    [
     #                        dbc.Row(
     #                            [
     #                                dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
     #                            ]
     #                        )
     #                    ],
     #                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
     #                ),
                    html.Div(
                        [
                            card_performance_measure_setup(app),
                        ]
                    ),                  
                ]
            )


def card_performance_measure_setup(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        card_recommended_carve_outs(app),
                        # card_summary_improvement(app),
                        card_medical_cost_target(app),
                        card_sl_sharing_arrangement(app),
                        card_quality_adjustment(app),
                        html.Div(
                            [
                                dbc.Button("RESET",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem", "width":"8rem","padding":"1rem","margin-right":"1rem"},
                                    id = 'button-reset-simulation',
                                    href='#top'
                                ),
                                dbc.Button("SUBMIT",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem", "width":"8rem", "padding":"1rem","margin-left":"1rem"},
                                    id = 'button-submit-simulation',
                                    href='#top'
                                ),
                            ],
                            style={"text-align":"center"}
                        )
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )


checklist = dbc.FormGroup(
    [
        dbc.Label("Recommended Carve-Outs"),
        dbc.Checklist(
            options=[
                {"label": "ESRD", "value": 1},
                {"label": "Cancer Patients", "value": 2},
                {"label": "HighCost Outliers(above 99th percentile)", "value": 3},
                {"label": "Transplant", "value": 4},
                {"label": "Trauma", "value": 5},
                {"label": "High Cost Specialty Drugs", "value": 6},
                {"label": "Mental Heaalth", "value": 7},
                {"label": "High Cost Implantable Devices", "value": 8},
                {"label": "Out of area Services", "value": 9},
            ],
            value=[1],
            id="carve-outs-checklist-input",
            inline=True,
        ),
    ]
)


def card_recommended_carve_outs(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Carve-Outs", style={"font-size":"1rem", "margin-left":"10px"}), width="auto"),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button("Carve-out Details", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"10rem","margin-left":"4rem"}, id="open-carve-outs-modal"),
                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader("Carve Out Details"),
                                                    dbc.ModalBody(
                                                        html.Div([tbl_carve_out_dtl(df_carve_out_details)], style={"padding-left":"2rem", "padding-right":"2rem", "padding-bottom":"4rem"})
                                                    ),
                                                    dbc.ModalFooter(
                                                        dbc.Button(
                                                            "Close", id="close-carve-outs-modal", className="ml-auto"
                                                        )
                                                    ),
                                                ],
                                                id="carve-outs-modal",
                                                size="xl",
                                                scrollable=True
                                            )
                                        ]
                                    )
                                    , width="auto"
                                ),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Form([checklist]),
                                                    html.Div(id="carve-outs-checklist", hidden=True),
                                                ]
                                            )
                                        ],
                                        style={"background-color":"#fff", "border-radius":"0.5rem","border":"none","padding":"1rem","max-height":"25rem","margin-top":"1rem","font-family": 'NotoSans-Regular',"font-size": "0.8rem"}
                                    ),
                                    style={"padding-left":"2rem","padding-right":"1rem"}
                                ),
                                
                            ]
                        )
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def card_summary_improvement(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Summary of Improvement Opportunities", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Row(
                                                [
                                                    # dbc.Col(html.H3("\u0024", style={"font-size":"1em","margin-top":"-1.2rem","color":"#1357DD"}), width="auto"),
                                                    dbc.Col(html.H3("\u0024 Cost Reduction", style={"font-size":"1em","color":"#1357DD","margin-left":"-2rem"})),
                                                ],
                                                style={"margin-top":"-1.6rem","margin-left":"-3rem","background-color":"#f5f5f5","width":"12rem","height":"3rem","padding-left":"0.5rem","padding-right":"0.5rem","text-align":"center"}
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("Overuse Reduction", style={"height":"1.8rem"}),
                                                                html.H1("1.0%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                        
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("Service Optimization", style={"height":"1.8rem"}),
                                                                html.H1("0.4%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("Transition of Care Management", style={"height":"1.8rem"}),
                                                                html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("Chronic Disease Management", style={"height":"1.8rem"}),
                                                                html.H1("1.2%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("High Risk Patient Management", style={"height":"1.8rem"}),
                                                                html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                    ),
                                                ]
                                            )
                                        ],
                                        style={"border-radius":"0.5rem","border":"2px solid #91b2ff","padding":"1rem","max-height":"25rem","margin-top":"1rem"}
                                    ),
                                    width=9,
                                    style={"padding-left":"2rem","padding-right":"1rem"}
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Row(
                                                [
                                                    
                                                    dbc.Col(html.H3("\u0024 Revenue Improvement", style={"font-size":"1em","color":"#1357DD","margin-left":"-2rem"})),
                                                ],
                                                style={"margin-top":"-1.6rem","margin-left":"-3rem","background-color":"#f5f5f5","width":"14rem","height":"3rem","padding-left":"0.5rem","padding-right":"0.5rem","text-align":"center"}
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.H6("Coding Improvement Opportunity", style={"height":"1.8rem"}),
                                                                html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                                            ],
                                                            style={"padding-left":"1rem", "padding-right":"1rem", "text-align":"center"}
                                                        ),
                                                    ),
                                                ]
                                            )
                                        ],
                                        style={"border-radius":"0.5rem","border":"2px solid #91b2ff","padding":"1rem","max-height":"25rem","margin-top":"1rem"}
                                    ),
                                    width=3,
                                    style={"padding-left":"2rem","padding-right":"1rem"}
                                ),
                            ]
                        )
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_medical_cost_target(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Medical Cost Target", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(),
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H4("Baseline", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.H4("ACO's Cost", style={"font-size":"0.8rem"})),
                                                        dbc.Col(html.H4("Benckmark Cost", style={"font-size":"0.8rem"})),
                                                        dbc.Col(html.H4("Best in-Class Cost", style={"font-size":"0.8rem"})),
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            [
                                                                "Target ",
                                                            ],
                                                            style={"font-size":"1rem"}
                                                        ),
                                                    ],
                                                ),
                                                html.Hr(className="ml-1"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    [
                                                                        "Recommended ",
                                                                        html.Span(
                                                                            "\u24D8",
                                                                            style={"font-size":"0.8rem"}
                                                                        )
                                                                    ],
                                                                    id="tooltip-vbc-measure",
                                                                    style={"font-size":"0.8rem"}
                                                                ),
                                                                dbc.Tooltip(
                                                                    "Cost target recommended for ACO to achieve reasonable margin improvement with high likelihood compared to FFS contract",
                                                                    target="tooltip-vbc-measure",
                                                                    style={"text-align":"start"}
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(html.H4("User Defined", style={"font-size":"0.8rem"})),
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H4("Likelihood to achieve", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.H4("Recommended", style={"font-size":"0.8rem"})),    
                                                        dbc.Col(html.H4("User Defined", style={"font-size":"0.8rem"})),
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                            ],
                            style={"padding-right":"0rem", "padding-left":"0rem"}
                        ),
                        
                        card_med_cost_target(),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def card_med_cost_target():
    return dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H6("Medical Cost Trend"), width=4),
                                dbc.Col(
                                    html.Div(id='bsl-trend'), width=4
                                ),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div(id="recom-trend")),
                                            dbc.Col([
                                                dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-tgt-trend', type = "number", debounce = True, step = 0.1, value = custom_input['medical cost target']['user target trend'],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                            ],
                                            style={"margin-top":"-0.5rem"}),

                                        ]
                                    )
                                    , width=4
                                ),
                            ],
                            style={"text-align":"center","padding-top":"1.5rem","padding-bottom":"0.5rem"},
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.H6("Medical Cost PMPM"), width=4),
                                dbc.Col(
                                    html.Div(id='bsl-pmpm'), width=4
                                ),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div(id="recom-pmpm")),
                                            dbc.Col(html.H6(custom_input['medical cost target']['user target'], id = 'div-usr-tgt')),
                                        ]
                                    )
                                    , width=4
                                ),
                                
                            ],
                            style={"text-align":"center","padding-top":"1rem",},
                        )
                    ],
                    width=9,
                    style={"background-color":"#fff","border-radius":"0.5rem","height":"6.8rem"},
                ),

                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.H1("High", id = 'div-recom-like',style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem", "color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"}), style={"padding-left":"1rem", "padding-right":"0.5rem"}, width=6),
                            dbc.Col(
#                                html.Div(html.H1("High",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"}),
                                id = 'div-usr-like', style={"padding-left":"0.5rem", "padding-right":"0.5rem"}, width=6),
                        ]
                    ),
                    width=3
                )
            ]
        )

def card_sl_sharing_arrangement(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("Shared Savings", style={"font-size":"1rem"}),
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(),width=5),
                                                dbc.Col(html.H6("Recommended"),width=3),
                                                dbc.Col(html.H6("User Defined"),width=4),
                                            ],
                                            style={"text-align":"center"},
                                            
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("MSR (Minimum Savings Rate)", style={"font-size":"0.8rem"}),width=5),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom msr']),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-msr', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['msr'],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("ACO's Sharing", style={"font-size":"0.8rem"}),width=3),
                                                dbc.Col(dbc.Checklist(options = [{'label':'Quality Adjustment', 'value' : 'selected'}], value = custom_input['savings/losses sharing arrangement']['saving qa'], id = 'switch-saving-method', style={"font-family":"NotoSans-Regular","font-size":"0.8rem"},
                                                    persistence = True, 
                                                    persistence_type = 'memory',))
                                            ],
                                            style={"padding-top":"1rem"}),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.Div(id = 'text-saving'),width=4),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings sharing']),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['savings sharing'],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.H5("Min Sharing %", id = 'text-saving-min', style={"font-size":"0.8rem"}),width=4),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings sharing min'],id = 'text-saving-min-recom'),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-min', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['savings sharing min'],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(html.H5("Sharing Method", style={"font-size":"0.8rem"}),width=4),
                                            dbc.Col(dcc.Dropdown(id = 'dropdown-firstdollar-saving', 

                                                options = [{'label': 'First Dollar Sharing', 'value': 'First Dollar Sharing'}, {'label':'Second Dollar Sharing (Above MSR)','value' : 'Second Dollar Sharing (Above MSR)'}],
                                                value = custom_input["savings/losses sharing arrangement"]["saving sharing method"],
                                                persistence = True, 
                                                persistence_type = 'memory',
                                                style={"font-size":"0.8rem"}), width = 7),
#                                            dbc.Col(html.H5("Second Dollar Sharing (Above MSR)", id = 'text-saving-right',style={"font-size":"0.6rem"}),width=4),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            ],
                                             style={"padding-top":"3.2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("Shared Savings Cap", style={"font-size":"0.8rem"}),width=5),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings share cap']),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['savings share cap'],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                    ],
                                    style={"border-radius":"0.5rem", "background-color":"#fff", "padding":"1rem"}
                                ),
                                dbc.Col(width=1),
                                dbc.Col(
                                    [
                                        dbc.Checklist(
                                            options = [{'label': "Shared Losses", 'value': 'Shared Losses'}], 
                                            value = custom_input['savings/losses sharing arrangement']['two side value'],
                                            persistence = True, 
                                            persistence_type = 'memory',
                                            id = 'switch-share-loss',
                                            switch = True,
                                            style={"font-family":"NotoSans-CondensedLight"}),
                                        html.Hr(),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(),width=5),
                                                dbc.Col(html.H6("Recommended"),width=3),
                                                dbc.Col(html.H6("User Defined"),width=4),
                                            ],
                                            style={"text-align":"center"},
                                            
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("MLR (Minimum Losses Rate)", style={"font-size":"0.8rem"}),width=5),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom mlr']),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-mlr', type = "number", step = 0.1, debounce = True, value = custom_input['savings/losses sharing arrangement']['mlr'], 
#                                                        disabled = not custom_input["savings/losses sharing arrangement"]["two side"],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.H2("ACO's Sharing", style={"font-size":"0.8rem"}),width=3),
                                            dbc.Col(dbc.Checklist(options = [{'label':'Quality Adjustment', 'value' : 'selected'}], 
                                                value = custom_input['savings/losses sharing arrangement']['losses qa'], id = 'switch-loss-method',style={"font-family":"NotoSans-Regular","font-size":"0.8rem"},
                                                persistence = True, 
                                                persistence_type = 'memory',))
                                            ],
                                            style={"padding-top":"1rem"}),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.Div("Min Sharing % (When quality targets are met)", id = 'text-loss'),width=4),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses sharing min']),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l-min', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['losses sharing min'], 
#                                                        disabled = not custom_input["savings/losses sharing arrangement"]["two side"],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.H5("Max Sharing %", style={"font-size":"0.8rem"}, id = 'text-loss-max'),width=4),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses sharing'], id = 'text-loss-max-recom'),style={"text-align":"center"},width=3),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['losses sharing'], 
#                                                        disabled = not custom_input["savings/losses sharing arrangement"]["two side"],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                         dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(html.H5("Sharing Method", style={"font-size":"0.8rem"}),width=4),
                                            dbc.Col(dcc.Dropdown(id = 'dropdown-firstdollar-loss', 

                                                options = [{'label': 'First Dollar Sharing', 'value': 'First Dollar Sharing'}, {'label':'Second Dollar Sharing (Below MLR)','value' : 'Second Dollar Sharing (Below MLR)'}],
                                                value = custom_input["savings/losses sharing arrangement"]["loss sharing method"],
                                                style={"font-size":"0.8rem"}, 
#                                                disabled = not custom_input["savings/losses sharing arrangement"]["two side"],
                                                persistence = True, 
                                                persistence_type = 'memory',), width = 7),
#                                            dbc.Col(html.H5("Second Dollar Sharing (Below MLR)", id = 'text-loss-right',style={"font-size":"0.6rem"}),width=4),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(dbc.Checklist(options = [{'label':"1 - Quality Adjusted Sharing Rate (CMS MSSP Enhanced Track Methodology)", 'value':"Quality Adjusted Sharing Rate"}], id = 'switch-quality-adj-rate',style={"font-family":"NotoSans-Regular","font-size":"0.8rem"},
                                                persistence = True, 
                                                persistence_type = 'memory',)),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("Shared Losses Cap", style={"font-size":"0.8rem"}),width=4),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses share cap']),style={"text-align":"center"},width=4),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap-l', type = "number", debounce = True, value = custom_input['savings/losses sharing arrangement']['losses share cap'], 
#                                                        disabled = not custom_input["savings/losses sharing arrangement"]["two side"],
                                                        persistence = True, 
                                                        persistence_type = 'memory',),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                    ],
                                    style={"border-radius":"0.5rem", "background-color":"#fff", "padding":"1rem"}
                                ),
                            ],
                            style={"padding-left":"2rem", "padding-right":"2rem", "padding-top":"1rem", "padding-bottom":"1rem"}
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_quality_adjustment(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Quality Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width=2),
                                dbc.Col(dbc.Button("Edit", className="mb-3",
                                            style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"4rem"},
                                            id = 'button-show-meas')),
                                
                            ],
                            no_gutters=True,
                        ),
                        html.Div([
                            html.Div([qualitytable(custom_input['quality adjustment']['user data'],custom_input['quality adjustment']["selected measures"])],id='container-measure-setup', style={"padding-bottom":"1rem"}),
                            dbc.Row(
                                [
                                    dbc.Col(html.H2("Total Weight", style={"font-size":"1rem", "margin-left":"10px"}), width=10),
                                    dbc.Col(html.Div("100%", id = 'div-recom-overall', style={"text-align":"center","background-color":"#fff","border-radius":"8rem","font-size":"0.8rem"}), style={"padding-left":"3.5rem","padding-right":"0.5rem"}),
                                    dbc.Col(html.Div("100%", id ='div-usr-overall', style={"text-align":"center","background-color":"#fff","border-radius":"8rem","font-size":"0.8rem"}), style={"padding-left":"0.5rem"}),
                                ],
                                no_gutters=True,
                                style={"padding-right":"0.5rem","padding-top":"0.5rem", "padding-bottom":"0.2rem", "background-color":"#bbd4ff", "border-radius":"10rem","width":"101.5%"}
                            ),], id = 'div-meas-table-container', hidden = True, style={"padding-left":"4rem", "padding-right":"1rem"}),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )



def tab_result(app):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H1("VBC Contract Simulation Result", style={"padding-left":"0rem","font-size":"1.8rem"})),
                            dbc.Col([
                                dbc.Button("View Scenario Assumptions",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"0.25rem", "font-family":"NotoSans-Regular", "font-size":"1rem"},
                                    id = 'button-open-assump-modal'
                                ),
                                dbc.Modal([
                                    dbc.ModalHeader(html.H1("Key Simulation Assumptions", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
                                    dbc.ModalBody([sim_assump_input_session(),]),
                                    dbc.ModalFooter(
                                        dbc.Button('Close', id = 'button-close-assump-modal'))
                                    ], id = 'modal-assump', size = 'xl', backdrop = 'static'),
                                ],
                                width="auto"
                            ),
                            # dbc.Col(
                            #     [
                            #         dbc.DropdownMenu(
                            #         label = 'Choose Version to Generate Contract',
                            #         children = [
                            #                         dbc.DropdownMenuItem('User Defined Setting', 
                            #                             href = '/vbc-demo/contract-generator/', 
                            #                             id = 'dropdownmenu-contract-gen'),
                            #                         dbc.DropdownMenuItem('Recommended Setting',
                            #                             href = '/vbc-demo/contract-generator-recommend/')
                            #                     ],
                            #         style={"font-family":"NotoSans-Regular", "font-size":"1rem"},
                            #         color="warning"
                            #         )
                            #     ]
                            # )
                            
                        ],
                        style={"padding-left":"2rem"}
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Plan's Cost Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                            id = 'dropdown-cost',
                                            options = [
                                            {'label' : "Plan's Total Cost", 'value' : "Plan's Total Cost" },
                                            {'label' : "ACO's Total Cost", 'value' : "ACO's Total Cost" },
                                            {'label' : "ACO's PMPM", 'value' : "ACO's PMPM" },
                                            ],#{'label' : "Plan's Total Revenue", 'value' : "Plan's Total Revenue" }
                                            value = "ACO's PMPM",
                                            ))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Graph(id = 'figure-cost', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"24rem", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-cost'), width=7),
                                        ],
                                        no_gutters=True,
                                    ),
                                    style={"padding":"1rem"}
                                )
                                
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        ),
                        style={"padding-top":"1rem"}
                    ),
                    
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("ACO's Financial Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                            id = 'dropdown-fin',
                                            options = [
                                            {'label' : "ACO's Total Revenue", 'value' : "ACO's Total Revenue" },
                                            {'label' : "ACO's Margin", 'value' : "ACO's Margin" },
                                            {'label' : "ACO's Margin %", 'value' : "ACO's Margin %" }],
                                            value = "ACO's Margin",
                                            ))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Graph(id = 'figure-fin', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"24rem", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-fin'), width=7),
                                        ],
                                        no_gutters=True,
                                    ),
                                    style={"padding":"1rem"}
                                )
                                
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        )
                    ),
                    html.Hr(),
                    html.H1(
                        "\u25c9 Best case scenario means more cost reduction is achieved in performance year than expected",
                        style={"font-size":"0.8rem"}
                    ),
                    html.H1(
                        "\u25c9Worst case scenario means less cost reduction is achieved in performance year than expected",
                        style={"font-size":"0.8rem"}
                    )
                ],
                style={"padding-top":"2rem","padding-bottom":"2rem","padding-left":"1rem","padding-right":"1rem"}

        )

def sim_assump_input_session():
    return html.Div([
        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Additional Patients Steered to ACO", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "0%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Medical Cost Trend (without management)", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "5.6%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),
        
        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Assumed Cost Trend Reduction", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "-2.4%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Coding Improvement", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "0.7%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            html.Div(
                [
                dbc.Row([
                    dbc.Col(html.H1("Quality Improvement", style={"font-size":"1rem"})),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Patient/ Caregiver Experience", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("CAHPS: Getting Timely Care, Appointments, and Information"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: How Well Your Providers Communicate"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Patients’ Rating of Provider"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Access to Specialists"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Health Promotion and Education"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Shared Decision Making"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Health Status/Functional Status"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Stewardship of Patient Resources"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Courteous and Helpful Office Staff"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Care Coordination"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Care Coordination/ Patient Safety", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Risk-Standardized, All Condition Readmission"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("All-Cause Unplanned Admissions for Patients with Multiple Chronic Conditions"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Ambulatory Sensitive Condition Acute Composite (AHRQ Prevention Quality Indicator (PQI)#91)"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Falls: Screening for Future Fall Risk"),
                            dbc.Col([dbc.Input(value = "15%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Preventive Health", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening: Influenza Immunization"),
                            dbc.Col([dbc.Input(value = "25%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening:Tobacco Use: Screening and Cessation Intervention"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening:Screening for Depression and Follow-up Plan"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Colorectal Cancer Screening"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Breast Cancer Screening"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Statin Therapy for the Prevention and Treatment of Cardiovascular Disease"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("At-Risk Population", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Depression Remission at Twelve Months"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Diabetes Mellitus: Hemoglobin A1c Poor Control"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Hypertension (HTN): Controlling High Blood Pressure"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                ],
                style={"background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("ACO's Margin under FFS", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "5%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),
        

        
        ]
    )


layout = create_layout(app)
#app.layout = create_layout(app)

'''@app.callback(
    Output('load-file', 'children'),
    [Input('interval-load-file', 'n_intervals')]
    )
def live_load_file(n):
    return load_files()
'''

### Carve Out ###
@app.callback(
    [
    Output("carve-outs-checklist", "children"),
    Output("temp-carveout", "children"),
    Output("bsl-trend", "children"),
    Output("bsl-pmpm", "children"),
    Output("recom-trend", "children"),
    Output("recom-pmpm", "children")
    ],
    [
        Input("carve-outs-checklist-input", "value"),
    ]
)
def on_change_recommended_carve_outs(checklist_value):
    checklist_str = 'c'
    maxlength = 9
    for ml in range(maxlength):
        if ml+1 in checklist_value:
            checklist_str += '1'
        else:
            checklist_str += '0'

    carve_code = {'code':checklist_str}

    data = df_carve_out[df_carve_out['code'] == checklist_str]

    bsl_trend = dbc.Row(
        [
            dbc.Col(html.H6("{:.1f}%".format(data['bsl_aco_trend'].values[0]*100))),
            dbc.Col(html.H6("{:.1f}%".format(data['bsl_benchmark_trend'].values[0]*100))),
            dbc.Col(html.H6("{:.1f}%".format(data['bsl_benchbest_trend'].values[0]*100))),
        ]
    )

    bsl_pmpm = dbc.Row(
        [
            dbc.Col(html.H6("${:.0f}".format(data['bsl_aco_pmpm'].values[0]))),
            dbc.Col(html.H6("${:.0f}".format(data['bsl_benchmark_pmpm'].values[0]))),
            dbc.Col(html.H6("${:.0f}".format(data['bsl_benchbest_pmpm'].values[0]))),
        ]
    )

    recom_trend = html.H6("{:.1f}%".format(data['recom_tar_trend'].values[0]*100))

    recom_pmpm = html.H6("${:.0f}".format(data['recom_tar_pmpm'].values[0]))

    return [checklist_str, json.dumps(carve_code), bsl_trend, bsl_pmpm, recom_trend, recom_pmpm]


@app.callback(
    Output("carve-outs-modal", "is_open"),
    [Input("open-carve-outs-modal", "n_clicks"), Input("close-carve-outs-modal", "n_clicks")],
    [State("carve-outs-modal", "is_open")],
)
def toggle_modal_recommended_carve_out(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

###
@app.callback(
    [Output('text-saving', 'children'),
    Output('input-usr-planshare-min', 'disabled'),
    Output('text-saving-min', 'style'),
    Output('text-saving-min-recom', 'style')],
    [Input('switch-saving-method', 'value')]
    )
def toggle_saving_method(v):
    if v and len(v)>0:
        return [html.H5("Max Sharing % (When quality targets are met)", style={"font-size":"0.8rem"})], False,{"font-size":"0.8rem"},{}
    return [html.H5("Sharing %", style={"font-size":"0.8rem"})],True,{"font-size":"0.8rem", "color":'#919191'},{"color":'#919191'}

@app.callback(
    [Output('text-loss', 'children'),
    Output('input-usr-planshare-l', 'disabled'),
    Output('text-loss-max', 'style'),
    Output('text-loss-max-recom', 'style'),
    Output('switch-quality-adj-rate', 'options')],
    [Input('switch-loss-method', 'value'),
    Input('switch-share-loss', 'value'),
    Input('button-reset-simulation', 'n_clicks')]
    )
def toggle_loss_method(v, v1, n):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'button-reset-simulation':
        return [html.H5("Min Sharing % (When quality targets are met)", style={"font-size":"0.8rem"})], True, {"font-size":"0.8rem"},{}, [{'label':"1 - Quality Adjusted Sharing Rate (CMS MSSP Enhanced Track Methodology)", 'value':"Quality Adjusted Sharing Rate", 'disabled':True}]
    elif 'Shared Losses' not in v1:
        return [html.H5("Min Sharing % (When quality targets are met)", style={"font-size":"0.8rem"})], True,{"font-size":"0.8rem"},{}, [{'label':"1 - Quality Adjusted Sharing Rate (CMS MSSP Enhanced Track Methodology)", 'value':"Quality Adjusted Sharing Rate", 'disabled':True}]
    else:
        if v and len(v)>0:
            return [html.H5("Min Sharing % (When quality targets are met)", style={"font-size":"0.8rem"})], False,{"font-size":"0.8rem"},{}, [{'label':"1 - Quality Adjusted Sharing Rate (CMS MSSP Enhanced Track Methodology)", 'value':"Quality Adjusted Sharing Rate", 'disabled':False}]
        else:
            return [html.H5("Sharing %", style={"font-size":"0.8rem"})],True,{"font-size":"0.8rem", "color":'#919191'},{"color":'#919191'}, [{'label':"1 - Quality Adjusted Sharing Rate (CMS MSSP Enhanced Track Methodology)", 'value':"Quality Adjusted Sharing Rate", 'disabled':True}]



@app.callback(
    [Output('input-usr-mlr', 'disabled'),
#    Output('input-usr-planshare-l', 'disabled'),
    Output('input-usr-sharecap-l', 'disabled'),
    Output('input-usr-planshare-l-min', 'disabled'),
    Output('dropdown-firstdollar-loss', 'disabled'),
    Output('switch-loss-method', 'options')],
    [Input('switch-share-loss', 'value'),
    Input('button-reset-simulation', 'n_clicks')]
    )
def toggle_share_loss(v,n):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'button-reset-simulation':
        return True, True, True, True, [{'label':'Quality Adjustment', 'value' : 'selected', 'disabled' : True}]
    elif 'Shared Losses' in v:
        return False, False, False, False, [{'label':'Quality Adjustment', 'value' : 'selected'}]
    else:
        return True, True, True, True, [{'label':'Quality Adjustment', 'value' : 'selected', 'disabled' : True}]


@app.callback(
    Output('div-meas-table-container', 'hidden'),
    [Input('button-show-meas', 'n_clicks')],
    [State('div-meas-table-container', 'hidden')]
    )
def show_meas_table(n, hidden):
    if n:
        return not hidden 
    return hidden

@app.callback(
    Output('div-usr-tgt', 'children'),
    [Input('input-usr-tgt-trend', 'value'),
    Input('button-reset-simulation', 'n_clicks')]
    )
def update_usr_target(v, n):
    base = default_input['medical cost target']['medical cost pmpm']
    base = int(base.replace("$",""))
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'button-reset-simulation':
        return default_input['medical cost target']['recom target']
    elif v:
        tgt = int(round(base*v/100+base,0))
        return '$'+str(tgt)
    else:
        return '$'+str(base)
   

@app.callback(
    Output('div-usr-like', 'children'),
    [Input('input-usr-tgt-trend', 'value'),
    Input('button-reset-simulation', 'n_clicks')]
    )
def cal_usr_like(usr_tgt, n):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'button-reset-simulation':
        return html.Div(html.H1("High",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"})
    elif usr_tgt:
#        recom_tgt_int = int(recom_tgt.replace('$','').replace('%','').replace(',',''))
#        usr_tgt_int = int(usr_tgt.replace('$','').replace('%','').replace(',',''))
        if usr_tgt >= 3.9:
            return html.Div(html.H1("High",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"})
        elif usr_tgt < 2.5:
            return html.Div(html.H1("Low",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"red"})
        else:
            return html.Div(html.H1("Mid",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem"}), style={"border-radius":"0.5rem", "background-color":"#F5B111"})
    else:
        return html.Div(html.H1("High",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"})


@app.callback(
    Output('modal-assump', 'is_open'),
    [Input('button-open-assump-modal', 'n_clicks'),
    Input('button-close-assump-modal', 'n_clicks'),],
    [State('modal-assump', 'is_open')]
    )
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('div-recom-overall', 'children'),
    Output('div-usr-overall', 'children')],
    [Input('table-measure-setup', 'data'),]
    )
def cal_overall_weight(data):
    
    df = pd.DataFrame(data)
    recom_overall = np.sum(int(i.replace('%','')) for i in list(df.fillna('0%').iloc[:,7]))
    usr_overall = np.sum(0 if i.replace('%','')=='' else int(i.replace('%','')) for i in list(df.fillna('0%').iloc[:,8]))
    return str(recom_overall)+'%', str(usr_overall)+'%'

# table style update on selected_rows
@app.callback(
    [Output('table-measure-setup', 'dropdown_conditional'),
    Output('table-measure-setup', 'style_data_conditional'),
    Output('table-measure-setup', 'data'),],
    [Input('table-measure-setup', 'selected_rows'),
    Input('table-measure-setup', 'data_timestamp'),],
    [State('table-measure-setup', 'data'),]
    )
def update_columns(selected_quality,timestamp, data):
    for i in range(0,23):
        row=data[i]

        if i in [4,11,16,21]:  
            row['userdefined']=str(row['userdefined']).replace('$','').replace('%','').replace(',','')+'%'
        else:
            row['userdefined']=float('nan')

        if i in selected_quality:
 
            if (row['tar_user_type'] is None) or (row['tar_user_type'] is np.nan):
                row['tar_user']=row['tar_recom']
                if i in [6,8,9,15,16,19,20]:
                    row['tar_user_type']='Report'
                else:
                    row['tar_user_type']='Performance'

            elif row['tar_user_type']=='Report':
                row['tar_user']='R'
            elif row['tar_user_type']=='Performance' and  row['tar_user']=='R':
                if row['tar_recom']=='R':
                    row['tar_user']=row['bic']

                else:
                    row['tar_user']=row['tar_recom']
            else:
                if i in range(10,23):
                    row['tar_user']=str(row['tar_user']).replace('$','').replace('%','').replace(',','')+'%'


        else:
            row['tar_user']=np.nan
            row['tar_user_type']=np.nan


    return qualitytable_dropdown_conditional(selected_quality),qualitytable_data_conditional(selected_quality),data


# store data
@app.callback(
    Output('temp-data', 'children'),
    [Input('div-usr-tgt', 'children'),
    Input('input-usr-tgt-trend', 'value'),
    Input('input-usr-msr', 'value'),
    Input('input-usr-planshare', 'value'),
    Input('input-usr-planshare-min', 'value'),
    Input('input-usr-sharecap', 'value'),
    Input('input-usr-mlr', 'value'),
    Input('input-usr-planshare-l', 'value'),
    Input('input-usr-planshare-l-min', 'value'),
    Input('input-usr-sharecap-l', 'value'),
    Input('switch-share-loss', 'value'),
    Input('switch-loss-method', 'value'),
    Input('table-measure-setup', 'selected_rows'),
    Input('table-measure-setup', 'data'),
    Input('dropdown-firstdollar-saving', 'value'),
    Input('dropdown-firstdollar-loss', 'value'),
    Input('switch-saving-method', 'value'),
#    Input('interval-load-file', 'n_intervals')
    ]
    )
def store_data(usr_tgt_int, usr_tgt_trend, usr_msr, usr_planshare, usr_planshare_min, usr_sharecap, usr_mlr, usr_planshare_l, usr_planshare_l_min, usr_sharecap_l, ts, lm, select_row, data, sharemethod, sharemethod_l, sm):
    global  custom_input

    df = pd.DataFrame(data)

    if 'Shared Losses' in ts:
        two_side = True
    else:
        two_side = False

    if 'selected' in lm:
        loss_method = True
    else:
        loss_method = False

    try: 
        usr_tgt = int(usr_tgt_int.replace('$',""))
    except:
        usr_tgt = int(usr_tgt_int)

    recom_dom_1 = int(df.iloc[4,7].replace('%',""))/100
    recom_dom_2 = int(df.iloc[11,7].replace('%',""))/100
    recom_dom_3 = int(df.iloc[16,7].replace('%',""))/100
    recom_dom_4 = int(df.iloc[21,7].replace('%',""))/100

    usr_dom_1 =(0 if df.iloc[4,8].replace('%','')=='' else int(df.iloc[4,8].replace('%',"")))/100
    usr_dom_2 =(0 if df.iloc[11,8].replace('%','')=='' else  int(df.iloc[11,8].replace('%',"")))/100
    usr_dom_3 =(0 if df.iloc[16,8].replace('%','')=='' else  int(df.iloc[16,8].replace('%',"")))/100
    usr_dom_4 =(0 if df.iloc[21,8].replace('%','')=='' else  int(df.iloc[21,8].replace('%',"")))/100

    user_tar_type=df['tar_user_type'].tolist()
    user_tar_value=df['tar_user'].tolist()


    datasets = {
        'medical cost target' : {'user target' : usr_tgt, "user target trend" : usr_tgt_trend},
        'savings/losses sharing arrangement' : {'two side' : two_side, 'two side value':ts, 'msr': usr_msr, 'savings sharing' : usr_planshare, 'savings sharing min' : usr_planshare_min, 'savings share cap' : usr_sharecap,
        'mlr' : usr_mlr, 'losses sharing' : usr_planshare_l, 'losses sharing min' : usr_planshare_l_min, 'losses share cap' : usr_sharecap_l, 'loss method' : loss_method, 'saving sharing method': sharemethod, 'loss sharing method' : sharemethod_l,  "saving qa":sm, "losses qa":lm},
        'quality adjustment' : {'selected measures' : select_row, 'recom_dom_1' : recom_dom_1, 'recom_dom_2' : recom_dom_2, 'recom_dom_3' : recom_dom_3, 'recom_dom_4' : recom_dom_4,
        'usr_dom_1' : usr_dom_1, 'usr_dom_2' : usr_dom_2, 'usr_dom_3' : usr_dom_3, 'usr_dom_4' : usr_dom_4,
        'user_tar_type':user_tar_type,'user_tar_value':user_tar_value, "user data" : data}
    }
    
    with open('configure/input_ds.json','w') as outfile:
        json.dump(datasets, outfile)

    custom_input = json.load(open('configure/input_ds.json', encoding = 'utf-8'))
    return json.dumps(datasets)

@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('temp-result', 'children')],
    [Input('button-submit-simulation', 'n_clicks')],
    [State('temp-data', 'children'),State('temp-carveout', 'children'),State('recom-pmpm', 'children')]
    )
def cal_simulation(submit, data, code, target_recom_pmpm):
    # carve_code = json.loads(code)['code']
    carve_code = eval(code)['code']
    if submit:
        datasets = json.loads(data)
        selected_rows = datasets['quality adjustment']['selected measures']
        domian_weight =list( map(datasets['quality adjustment'].get, ['usr_dom_1','usr_dom_2','usr_dom_3','usr_dom_4']) ) 
        target_user_pmpm = datasets['medical cost target']['user target']
        msr_user = datasets['savings/losses sharing arrangement']['msr']/100
        mlr_user = datasets['savings/losses sharing arrangement']['mlr']
        max_user_savepct = datasets['savings/losses sharing arrangement']['savings sharing']/100
        min_user_savepct = datasets['savings/losses sharing arrangement']['savings sharing min']/100
        max_user_losspct = datasets['savings/losses sharing arrangement']['losses sharing']
        min_user_losspct = datasets['savings/losses sharing arrangement']['losses sharing min']
        cap_user_savepct = datasets['savings/losses sharing arrangement']['savings share cap']/100
        cap_user_losspct = datasets['savings/losses sharing arrangement']['losses share cap']
        twosided = datasets['savings/losses sharing arrangement']['two side']
        lossmethod = datasets['savings/losses sharing arrangement']['loss method']
        user_tar_type=datasets['quality adjustment']['user_tar_type']
        user_tar_value=datasets['quality adjustment']['user_tar_value']

        if twosided == True:
            mlr_user = mlr_user/100
            max_user_losspct = max_user_losspct/100
            min_user_losspct = min_user_losspct/100
            cap_user_losspct = cap_user_losspct/100

        # print(carve_code, target_user_pmpm, target_recom_pmpm)

        df=simulation_cal(carve_code,df_carve_out,selected_rows,domian_weight,user_tar_type,user_tar_value,default_input,target_user_pmpm,target_recom_pmpm,msr_user,mlr_user,max_user_savepct,min_user_savepct,min_user_losspct,max_user_losspct,cap_user_savepct,cap_user_losspct,twosided,lossmethod)

        return 'tab-1', df.to_json(orient = 'split')
    return 'tab-0', ""

@app.callback(
    [Output('figure-cost', 'figure'),
    Output('table-cost', 'children')],
    [Input('dropdown-cost', 'value'),
    Input('temp-result', 'children')]
    )
def update_grapg_cost(metric, data):
    if data:
        dff = pd.read_json(data, orient = 'split')
        df = dff[dff['Metrics'] == metric]
        return sim_result_box(df), table_sim_result(df)
    return {},""

@app.callback(
    [Output('figure-fin', 'figure'),
    Output('table-fin', 'children')],
    [Input('dropdown-fin', 'value'),
    Input('temp-result', 'children')]
    )
def update_grapg_cost(metric, data):
    if data:
        dff = pd.read_json(data, orient = 'split')
        df = dff[dff['Metrics'] == metric]
        return sim_result_box(df),table_sim_result(df)
    return {}, ""


@app.callback(
    [Output('input-usr-tgt-trend', 'value'),
    Output('input-usr-msr', 'value'),
    Output('input-usr-planshare', 'value'),
    Output('input-usr-planshare-min', 'value'),
    Output('input-usr-sharecap', 'value'),
    Output('input-usr-mlr', 'value'),
    Output('input-usr-planshare-l', 'value'),
    Output('input-usr-planshare-l-min', 'value'),
    Output('input-usr-sharecap-l', 'value'),
    Output('switch-share-loss', 'value'),
    Output('switch-saving-method', 'value'),
    Output('switch-loss-method', 'value'),
    Output('dropdown-firstdollar-saving', 'value'),
    Output('dropdown-firstdollar-loss', 'value'),
    Output('table-measure-setup', 'selected_rows')],
#    Output('table-measure-setup', 'data'),],
    [Input('button-reset-simulation', 'n_clicks')]
    )
def reset_user_define(n):
    if n:
        msr = int(default_input['savings/losses sharing arrangement']['recom msr'].replace('"','').replace('%','').replace('$',''))
        saving_share = int(default_input['savings/losses sharing arrangement']['recom savings sharing'].replace('"','').replace('%','').replace('$',''))
        saving_share_min = int(default_input['savings/losses sharing arrangement']['recom savings sharing min'].replace('"','').replace('%','').replace('$',''))
        saving_share_cap = int(default_input['savings/losses sharing arrangement']['recom savings share cap'].replace('"','').replace('%','').replace('$','')[0:2])
        mlr = int(default_input['savings/losses sharing arrangement']['recom mlr'].replace('"','').replace('%','').replace('$',''))
        loss_share = int(default_input['savings/losses sharing arrangement']['recom losses sharing'].replace('"','').replace('%','').replace('$',''))
        loss_share_min = int(default_input['savings/losses sharing arrangement']['recom losses sharing min'].replace('"','').replace('%','').replace('$',''))
        loss_share_cap = int(default_input['savings/losses sharing arrangement']['recom losses share cap'].replace('"','').replace('%','').replace('$','')[0:2])
        return default_input['medical cost target']["user target"], msr, saving_share, saving_share_min, saving_share_cap, mlr,  loss_share,  loss_share_min,  loss_share_cap,   [], ["selected"], ["selected"], "First Dollar Sharing", "First Dollar Sharing",  [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    else:
        return custom_input['medical cost target']["user target trend"], custom_input['savings/losses sharing arrangement']['msr'], custom_input['savings/losses sharing arrangement']['savings sharing'], custom_input['savings/losses sharing arrangement']['savings sharing min'], custom_input['savings/losses sharing arrangement']['savings share cap'], custom_input['savings/losses sharing arrangement']['mlr'], custom_input['savings/losses sharing arrangement']['losses sharing'], custom_input['savings/losses sharing arrangement']['losses sharing min'], custom_input['savings/losses sharing arrangement']['losses share cap'], custom_input['savings/losses sharing arrangement']['two side value'], custom_input['savings/losses sharing arrangement']['saving qa'], custom_input['savings/losses sharing arrangement']['losses qa'], custom_input['savings/losses sharing arrangement']['saving sharing method'], custom_input['savings/losses sharing arrangement']['loss sharing method'],  custom_input['quality adjustment']['selected measures']



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8050)


