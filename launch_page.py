#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd
import numpy as np

from app import app
# import test_contract_opportunities
import test_contract_manager
import test_contract_manager_drilldown
import test_contract_manager_bundle
import test_contract_manager_drilldown_bundle
# import test_contract_optimizer
# import test_contract_optimizer_bundle
# import test_contract_generator
# import test_contract_generator_recom
# import test_contract_generator_bundle
import test_contract_manager_bundle
import test_contract_manager_drilldown_bundle
# import test_contract_report_generator
# import test_contract_report_generator_bundle
import contract_overview
import aco_contract
import bundle_contract




def launch_layout():
    return html.Div([

                    
                    html.Div(
                        [
                            html.Img(src=app.get_asset_url("logo-demo.png"),style={"height":"20rem","margin-top":"5rem"}),
                            html.H1(u"ValueGen Solution",style={"background-color":"transparent","font-size":"5rem"}),
                            html.Div([
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Button("ENTER", color="dark", className="mr-1", href = "/vbc-demo/contract-overview/", style={"font-family":"NotoSans-Black", "font-size":"1rem", "padding":"1rem","border-radius":"1rem","border":"none","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1)"}), style={"border-radius":"1rem","width":"5rem"}),
                                                # dbc.Col(dbc.Button("Contract Administrator", color="light", className="mr-1", href = "/vbc-demo/contract-manager/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem", "padding":"1rem", "border-radius":"1rem","border":"1px solid #ececf6","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1)"}), style={"border-radius":"1rem","width":"5rem"}),
                                                # dbc.Col(dbc.Button("Tele Case Manager", color="light", className="mr-1", href = "/vbc-demo/tele-case-manager/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem", "border-radius":"1rem","border":"1px solid #ececf6","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1)"}), style={"border-radius":"1rem","width":"5rem"}),
                                            ],
                                            style={"background-color":"none", "font-family":"NotoSans-Regular", "font-size":"1rem", "border":"none","padding-top":"1rem","padding-bottom":"1rem","padding-left":"20rem","padding-right":"20rem"}
                                        )
                                    ]
                                )

                            ],
                            style={"background-color":"transparent", "border":"none", "width":"1400px", "margin":"auto"}
                            ),
                        ],
                        style={"background-color":"transparent","text-align":"center"}
                    ),
                    html.Div(
                        [
                            html.P("© 2021 Powered by One Health Link ")
                        ],
                        style={"magin":"auto","position":"fixed","bottom":"0","width":"100%","text-align":"center", "font-size":"1rem"}
                    ),
                    
                ],
                style={"background-color":"#fff","height":"100vh"})#, "background-image":"linear-gradient(to bottom, rgba(105, 132, 214,0), rgba(105, 132, 214,1))"})


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/vbc-demo/contract-manager/":
        return test_contract_manager.layout
    elif pathname == "/vbc-demo/contract-manager-drilldown/":
        return test_contract_manager_drilldown.layout
    elif pathname == "/vbc-demo/contract-manager-bundle/":
        return test_contract_manager_bundle.layout
    elif pathname == "/vbc-demo/contract-manager-drilldown-bundle/":
        return test_contract_manager_drilldown_bundle.layout
    # elif pathname == "/vbc-demo/contract-optimizer-opportunities/":
    #     return test_contract_opportunities.layout
    # elif pathname == "/vbc-demo/contract-optimizer/":
    #     return test_contract_optimizer.layout
    # elif pathname == "/vbc-demo/contract-optimizer-bundle/":
    #     return test_contract_optimizer_bundle.layout
    # elif pathname == "/vbc-demo/contract-generator/":
    #     return test_contract_generator.layout
    # elif pathname == "/vbc-demo/contract-generator-recommend/":
    #     return test_contract_generator_recom.layout
    # elif pathname == "/vbc-demo/contract-generator-bundle/":
    #     return test_contract_generator_bundle.layout
    elif pathname == "/vbc-demo/contract-manager-bundle/":
        return test_contract_manager_bundle.layout
    elif pathname == "/vbc-demo/contract-manager-drilldown-bundle/":
        return test_contract_manager_drilldown_bundle.layout
    # elif pathname == "/vbc-demo/contract-manager/report-generator/":
    #     return test_contract_report_generator.layout
    # elif pathname == "/vbc-demo/contract-manager-bundle/report-generator/":
    #     return test_contract_report_generator_bundle.layout
    elif pathname == "/vbc-demo/contract-overview/":
        return contract_overview.layout
    elif pathname == "/vbc-demo/contract-optimizer/aco":
            return aco_contract.layout
    elif pathname == "/vbc-demo/contract-optimizer/bundle":
            return bundle_contract.layout
        
    else:
        return launch_layout()

#####################################3
     

if __name__ == "__main__":

    app.run_server(host='0.0.0.0',port=8099, debug=False)

                        
