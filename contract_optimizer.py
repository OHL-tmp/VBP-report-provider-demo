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

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *
from simulation_cal import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract_optimizer/')

server = app.server

file = open('configure/default_ds.json', encoding = 'utf-8')
default_input = json.load(file)
df_quality = pd.read_csv("data/quality_setup.csv")


def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_contract(app, True, False, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
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

                    
                ],
                style={"background-color":"#f5f5f5"},
            )


def tab_setup(app):
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("Contract Simulation Setup", style={"padding-left":"2rem","font-size":"3"}), width=9),
						],
                        style={"padding-top":"2rem"}
					),
					html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
                                ]
                            )
                        ],
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
                    ),
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
                        card_medical_cost_target(app),
                        card_sl_sharing_arrangement(app),
                        card_quality_adjustment(app),
                        html.Div(
                            dbc.Button("SUBMIT",
                                className="mb-3",
                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem", "width":"8rem"},
                                id = 'button-submit-simulation'
                            ),
                            style={"text-align":"center"}
                        )
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
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
                                						dbc.Col(html.H4("Member Count", style={"font-size":"0.8rem"})),
                                						dbc.Col(html.H4("Medical Cost PMPM", style={"font-size":"0.8rem"})),
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
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Likelihood to achieve", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col([
                                                            dbc.Button("Recommended", id = 'button-recom', color = 'link',style={"font-size":"0.8rem"}),
                                                            dbc.Popover([
                                                                dbc.PopoverHeader("Cost Target Setting"),
                                                                dbc.PopoverBody(dbc.ListGroup([
                                                                    dbc.Row([
                                                                        dbc.Col("(1) Medical Cost Trend (without management)"),
                                                                        dbc.Col("5.6%")]),
                                                                    html.Hr(),

                                                                    dbc.Row([
                                                                        dbc.Col("(2) Trend Adjustment"),
                                                                        dbc.Col("-2.4%")]),
                                                                    dbc.Row([
                                                                        dbc.Col("Overuse Reduction"),
                                                                        dbc.Col("-0.7%")]),
                                                                    dbc.Row([
                                                                        dbc.Col("Service Optimization"),
                                                                        dbc.Col("-0.2%")]),
                                                                    dbc.Row([
                                                                        dbc.Col("Transition of Care Management"),
                                                                        dbc.Col("-0.3%")]),
                                                                    dbc.Row([
                                                                        dbc.Col("Chronic Disease Management"),
                                                                        dbc.Col("-0.5%")]),
                                                                    dbc.Row([
                                                                        dbc.Col("High Risk Patient Management"),
                                                                        dbc.Col("-0.7%")]),
                                                                    html.Hr(),

                                                                    dbc.Row([
                                                                        dbc.Col("(3) Coding Improvement Opportunity"),
                                                                        dbc.Col("0.7%")]),
                                                                    html.Hr(),

                                                                    dbc.Row([
                                                                        dbc.Col("(4) Target Trend Increase from Baseline (4)=(1)+(2)+(3)"),
                                                                        dbc.Col("3.9%")]),
                                                                    html.Hr(),

                                                                    dbc.Row([
                                                                        dbc.Col("(5) Performance Year Spending Target (5)=baseline*(4)"),
                                                                        dbc.Col("$850")]),
                                                                    ])),
                                                                ], 
                                                                id = 'popover-recom', is_open = False, target = 'button-recom', placement = 'top')
                                                            ],
                                                            style={"margin-top":"-0.6rem"}),
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

                        dbc.Row(
                        	[
                        		dbc.Col(html.H6("Medical Cost Target"), width=3),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6(default_input['medical cost target']['member count'])),
                    						dbc.Col(html.H6(default_input['medical cost target']['medical cost pmpm'])),
                    					]
                    				)
                        			, width=3
                        		),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6(default_input['medical cost target']['recom target'], id = 'div-recom-tgt')),
                    						dbc.Col([
                                                dbc.InputGroup([
                                                    dbc.InputGroupAddon('$', addon_type = 'prepend'),
                                                    dbc.Input(id = 'input-usr-tgt', type = "number", debounce = True, value = default_input['medical cost target']['user target'])
                                                    ],
                                                    size="sm")
                                                ],
                                                style={"margin-top":"-0.5rem"}),
                    					]
                    				)
                        			, width=3
                        		),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6("High", id = 'div-recom-like')),
                    						dbc.Col(html.Div("Low", id = 'div-usr-like')),
                    					]
                    				)
                        			, width=3
                        		),
                        	],
                            style={"text-align":"center","padding-top":"1rem","padding-bottom":"0.8rem", "background-color":"#fff","border-radius":"0.5rem"},
                        )
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
	                    						dbc.Col(html.Div(),width=4),
	                    						dbc.Col(html.H6("Recommended"),width=4),
	                    						dbc.Col(html.H6("User Defined"),width=4),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("MSR (Minimum Savings Rate)", style={"font-size":"0.7rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom msr']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-msr', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['msr']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
				                        dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Plan's Sharing %", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings sharing']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['savings sharing']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Shared Savings Cap", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings share cap']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['savings share cap']),
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
                                            value = [], 
                                            id = 'switch-share-loss',
                                            switch = True,
                                            style={"font-family":"NotoSans-CondensedLight"}),
                                        html.Hr(),
                                		dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(),width=4),
	                    						dbc.Col(html.H6("Recommended"),width=4),
	                    						dbc.Col(html.H6("User Defined"),width=4),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("MSR (Minimum Savings Rate)", style={"font-size":"0.7rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom mlr']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-mlr', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['mlr']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
				                        dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Plan's Sharing %", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses sharing']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['losses sharing']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Shared Losses Cap", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses share cap']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap-l', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['losses share cap']),
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
                            html.Div([qualitytable(df_quality)], style={"padding-bottom":"1rem"}),
                            dbc.Row(
                                [
                                    dbc.Col(html.H2("Overall Weight", style={"font-size":"1rem", "margin-left":"10px"}), width=11),
                                    dbc.Col(html.Div("100%", id = 'div-recom-overall', style={"text-align":"center","background-color":"#fff","border-radius":"10rem","font-size":"0.8rem"}), style={"padding-right":"0.8rem"}),
                                    dbc.Col(html.Div("100%", id ='div-usr-overall', style={"text-align":"center","background-color":"#fff","border-radius":"10rem","font-size":"0.8rem"})),
                                ],
                                no_gutters=True,
                                style={"padding-right":"0.5rem","padding-top":"0.5rem", "padding-bottom":"0.2rem", "background-color":"#bbd4ff", "border-radius":"10rem","width":"101%"}
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
                            dbc.Col(html.H1("VBC Contract Simulation Result", style={"padding-left":"2rem","font-size":"3"}), width=9),
                            dbc.Col([
                                dbc.Button("Edit Scenario Assumptions",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem"},
                                    id = 'button-open-assump-modal'
                                ),
                            	dbc.Modal([
                            		dbc.ModalHeader(html.H1("Key Simulation Assumptions", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
                            		dbc.ModalBody([sim_assump_input_session(),]),
                            		dbc.ModalFooter(
                            			dbc.Button('Close', id = 'button-close-assump-modal'))
                            		], id = 'modal-assump', size = 'xl'),
                            	]),
                            
                        ]
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=6),
                                        dbc.Col(html.Div("Metric"), width=2),
                                        dbc.Col(dcc.Dropdown(
                                        	id = 'dropdown-cost',
                                        	options = [
                                        	{'label' : "Plan's Total Cost", 'value' : "Plan's Total Cost" },
                                        	{'label' : "ACO's Total Cost", 'value' : "ACO's Total Cost" },
                                        	{'label' : "ACO's PMPM", 'value' : "ACO's PMPM" },
                                        	],#{'label' : "Plan's Total Revenue", 'value' : "Plan's Total Revenue" }
                                            value = "Plan's Total Cost",
                                        	))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'figure-cost',style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-cost'), width=6),
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
                    
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=6),
                                        dbc.Col(html.Div("Metric"), width=2),
                                        dbc.Col(dcc.Dropdown(
                                        	id = 'dropdown-fin',
                                        	options = [
                                        	{'label' : "ACO's Total Revenue", 'value' : "ACO's Total Revenue" },
                                        	{'label' : "ACO's Margin", 'value' : "ACO's Margin" },
                                        	{'label' : "ACO's Margin %", 'value' : "ACO's Margin %" }],
                                            value = "ACO's Total Revenue",
                                        	))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'figure-fin',style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-fin'), width=6),
                                        ],
                                        no_gutters=True,
                                    ),
                                    style={"padding":"1rem"}
                                )
                                
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        )
                    )
                ],
                style={"padding-top":"2rem","padding-bottom":"2rem","padding-left":"1rem","padding-right":"1rem"}

        )

def sim_assump_input_session():
    return html.Div([
        dbc.Row([
            dbc.Col("Patient Steerage to ACO"),
            dbc.Col([dbc.Input(value = "0%",)])
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col("Medical Cost Trend (without management)"),
            dbc.Col([dbc.Input(value = "5.6%",)])
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col("Cost Trend Reduction"),
            dbc.Col([dbc.Input(value = "-2.4%",)])
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col("Coding Improvement"),
            dbc.Col([dbc.Input(value = "0.7%",)])
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col("Quality Improvement"),
            dbc.Col([dbc.Input(value = "9.5%",)])
            ]),
        dbc.Row([
            dbc.Col(["Patient/ Caregiver Experience"]),
            dbc.Col([
                dbc.Row([
                    dbc.Col("CAHPS: Getting Timely Care, Appointments, and Information"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: How Well Your Providers Communicate"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Patients’ Rating of Provider"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Access to Specialists"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Health Promotion and Education"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Shared Decision Making"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Health Status/Functional Status"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Stewardship of Patient Resources"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Courteous and Helpful Office Staff"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("CAHPS: Care Coordination"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                ]),
            ]),
        dbc.Row([
            dbc.Col(["Care Coordination/ Patient Safety"]),
            dbc.Col([
                dbc.Row([
                    dbc.Col("Risk-Standardized, All Condition Readmission"),
                    dbc.Col([dbc.Input(value = "20%")])]),
                dbc.Row([
                    dbc.Col("All-Cause Unplanned Admissions for Patients with Multiple Chronic Conditions"),
                    dbc.Col([dbc.Input(value = "20%")])]),
                dbc.Row([
                    dbc.Col("Ambulatory Sensitive Condition Acute Composite (AHRQ Prevention Quality Indicator (PQI)#91)"),
                    dbc.Col([dbc.Input(value = "20%")])]),
                dbc.Row([
                    dbc.Col("Falls: Screening for Future Fall Risk"),
                    dbc.Col([dbc.Input(value = "15%")])]),
                ]),
            ]),
        dbc.Row([
            dbc.Col(["Preventive Health"]),
            dbc.Col([
                dbc.Row([
                    dbc.Col("Preventive Care and Screening: Influenza Immunization"),
                    dbc.Col([dbc.Input(value = "25%")])]),
                dbc.Row([
                    dbc.Col("Preventive Care and Screening:Tobacco Use: Screening and Cessation Intervention"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("Preventive Care and Screening:Screening for Depression and Follow-up Plan"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("Colorectal Cancer Screening"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("Breast Cancer Screening"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                dbc.Row([
                    dbc.Col("Statin Therapy for the Prevention and Treatment of Cardiovascular Disease"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                ]),
            ]),
        dbc.Row([
            dbc.Col(["At-Risk Population"]),
            dbc.Col([
                dbc.Row([
                    dbc.Col("Depression Remission at Twelve Months"),
                    dbc.Col([dbc.Input(value = "0%")])]),
                dbc.Row([
                    dbc.Col("Diabetes Mellitus: Hemoglobin A1c Poor Control"),
                    dbc.Col([dbc.Input(value = "20%")])]),
                dbc.Row([
                    dbc.Col("Hypertension (HTN): Controlling High Blood Pressure"),
                    dbc.Col([dbc.Input(value = "10%")])]),
                ]),
            ]),

        ])


app.layout = create_layout(app)

@app.callback(
    Output('popover-recom', 'is_open'),
    [Input('button-recom', 'n_clicks')],
    [State('popover-recom', 'is_open')]
    )
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('input-usr-mlr', 'disabled'),
    Output('input-usr-planshare-l', 'disabled'),
    Output('input-usr-sharecap-l', 'disabled'),],
    [Input('switch-share-loss', 'value')]
    )
def toggle_share_loss(v):
    if 'Shared Losses' in v:
        return False, False, False
    return True, True, True

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
    [Output('div-usr-like', 'children'),
    Output('div-usr-like', 'style')],
    [Input('input-usr-tgt', 'value')],
    [State('div-recom-like', 'children'),
    State('div-recom-tgt', 'children')]
    )
def cal_usr_like(usr_tgt, recom_like, recom_tgt):
    if usr_tgt:
        recom_tgt_int = int(recom_tgt.replace('$','').replace('%','').replace(',',''))
        if usr_tgt >= recom_tgt_int:
            return 'High', {}
        elif usr_tgt < recom_tgt_int*0.95:
            return 'Low', {'background-color':'red'}
        else:
            return 'Mid', {}
    return '', {}

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
    usr_overall = np.sum(int(i.replace('%','')) for i in list(df.fillna('0%').iloc[:,8]))
    return str(recom_overall)+'%', str(usr_overall)+'%'

# set up table selfupdate
@app.callback(
    Output('table-measure-setup', 'data'),
    [Input('table-measure-setup', 'data_timestamp')],
    [State('table-measure-setup', 'data')])
def update_columns(timestamp, data):
    for i in range(0,23):
        row=data[i]
        if i in [4,11,16,21]:  
            row['userdefined']=str(row['userdefined']).replace('$','').replace('%','').replace(',','')+'%'
        else:
            row['userdefined']=float('nan')

    return data 

# store data
@app.callback(
	Output('temp-data', 'children'),
	[Input('input-usr-tgt', 'value'),
	Input('input-usr-msr', 'value'),
	Input('input-usr-planshare', 'value'),
	Input('input-usr-sharecap', 'value'),
	Input('input-usr-mlr', 'value'),
	Input('input-usr-planshare-l', 'value'),
	Input('input-usr-sharecap-l', 'value'),
    Input('switch-share-loss', 'value'),
    Input('table-measure-setup', 'selected_rows'),
    Input('table-measure-setup', 'data')]
	)
def store_data(usr_tgt, usr_msr, usr_planshare, usr_sharecap, usr_mlr, usr_planshare_l, usr_sharecap_l, ts, select_row, data):
    df = pd.DataFrame(data)

    if 'Shared Losses' in ts:
        two_side = True
    else:
        two_side = False

    recom_dom_1 = int(df.iloc[4,7].replace('%',""))/100
    recom_dom_2 = int(df.iloc[11,7].replace('%',""))/100
    recom_dom_3 = int(df.iloc[16,7].replace('%',""))/100
    recom_dom_4 = int(df.iloc[21,7].replace('%',""))/100

    usr_dom_1 = int(df.iloc[4,8].replace('%',""))/100
    usr_dom_2 = int(df.iloc[11,8].replace('%',""))/100
    usr_dom_3 = int(df.iloc[16,8].replace('%',""))/100
    usr_dom_4 = int(df.iloc[21,8].replace('%',""))/100

    datasets = {
        'medical cost target' : {'user target' : usr_tgt},
        'savings/losses sharing arrangement' : {'two side' : two_side, 'msr': usr_msr, 'savings sharing' : usr_planshare, 'savings share cap' : usr_sharecap,
        'mlr' : usr_mlr, 'losses sharing' : usr_planshare_l, 'losses share cap' : usr_sharecap_l},
        'quality adjustment' : {'selected measures' : select_row, 'recom_dom_1' : recom_dom_1, 'recom_dom_2' : recom_dom_2, 'recom_dom_3' : recom_dom_3, 'recom_dom_4' : recom_dom_4,
        'usr_dom_1' : usr_dom_1, 'usr_dom_2' : usr_dom_2, 'usr_dom_3' : usr_dom_3, 'usr_dom_4' : usr_dom_4}
    }
    
    with open('configure/input_ds.txt','w') as outfile:
        json.dump(datasets, outfile)
    return json.dumps(datasets)

@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('temp-result', 'children')],
    [Input('button-submit-simulation', 'n_clicks')],
    [State('temp-data', 'children')]
    )
def cal_simulation(submit, data):
    if submit:
        datasets = json.loads(data)
        selected_rows = datasets['quality adjustment']['selected measures']
        domian_weight =list( map(datasets['quality adjustment'].get, ['usr_dom_1','usr_dom_2','usr_dom_3','usr_dom_4']) ) 
        target_user_pmpm = datasets['medical cost target']['user target']
        msr_user = datasets['savings/losses sharing arrangement']['msr']/100
        mlr_user = datasets['savings/losses sharing arrangement']['mlr']
        max_user_savepct = datasets['savings/losses sharing arrangement']['savings sharing']/100
        max_user_losspct = datasets['savings/losses sharing arrangement']['losses sharing']
        cap_user_savepct = datasets['savings/losses sharing arrangement']['savings share cap']/100
        cap_user_losspct = datasets['savings/losses sharing arrangement']['losses share cap']
        twosided = datasets['savings/losses sharing arrangement']['two side']

        if twosided == True:
            mlr_user = mlr_user/100
            max_user_losspct = max_user_losspct/100
            cap_user_losspct = cap_user_losspct/100

        df=simulation_cal(selected_rows,domian_weight,target_user_pmpm,msr_user,mlr_user,max_user_savepct,max_user_losspct,cap_user_savepct,cap_user_losspct,twosided)

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

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)


