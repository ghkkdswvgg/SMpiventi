"""

SM.Pi Interface
Designed April 2020 during fight against COVID-19

Copyright Dead X-men Society

Strictly restricted to non-commercial use

"""

### --- MODULES --- ###


import sys
import time

import math
import random

import flask
import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input, Output, State

import plotly
import plotly.graph_objs as go


### --- SERIAL COMMUNICATION --- ###


# install pyserial
import serial
from serial import Serial

#ser = serial.Serial('/dev/ttyUSB0', 9600)                  # Raspberry Pi (USB0)
#ser = serial.Serial('/dev/cu.usbserial-14420', 9600)      # Mac OS (14420)
ser = serial.Serial('COM4', 9600)                            



### --- APP SETUP --- ###


server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

t_0 = time.time()  

app.title = 'SM venti'


### --- BODY --- ###


app.layout = html.Div([

    ### MAIN HEADER ###

    html.Div(id = 'header', children = [
        html.H1(children = 'SM.Pi | VC - AC'),
    ]),

    ### CONTAINER ###

    html.Div(id = 'container', className = 'container clearfix', children = [
        
        ### Graphs ###

        html.Div(id = 'graphs-box', className = 'column graphs-box', children = [

            # Graph 1 #

            html.Div(className = 'graph-title', children = [
                html.H2('Flow Rate (L/min)'),
            ]),

            html.Div(id = 'graph-1', className = 'graph', children = [
                html.Div(id = 'graph1box', className = 'graph-box-contents', children = [
                    dcc.Graph(id = 'live-graph1'),        
                ]),
            ]),

            # Graph 2 #

            html.Div(className = 'graph-title', children = [
                html.H2('Pressure (cmH₂0)'),
            ]),

            html.Div(id = 'graph-2', className = 'graph graph2', children = [
                html.H4(id = 'comingsoon', className = 'comingsoon', children = [
                    'Available in version 2.0 - Coming soon!',
                ]),
                html.Div(id = 'graph2box', className = 'graph-box-contents', children = [
                    dcc.Graph(id = 'live-graph2'),        
                ]),
            ]),

            # Constant And Derived Parameters #

            html.Div(className = 'constants', children = [
                html.Div(className = 'constants_first', children = [
                    html.Div(className = 'constant left', children = [
                        html.H3(className = 'quantity', children = 'IBW'),
                        html.Div(className = 'q-value', id='ibw'),
                        html.Label(className = 'unit', children = 'kg')
                    ]),
                    html.Div(className = 'constant right', children = [
                        html.H3(className = 'quantity', children = 'TV'),
                        html.Div(className = 'q-value', id='tv'),
                        html.Label(className = 'unit', children = 'mL')
                    ]),
                ]),
                html.Div(className = 'constants_second', children = [
                    html.Div(className = 'constant left', children = [
                        html.H3(className = 'quantity', children = 'MV'),
                        html.Div(className = 'q-value', id='mv'),
                        html.Label(className = 'unit', children = 'L/min')
                    ]),
                    html.Div(className = 'constant right', children = [
                        html.H3(className = 'quantity', children = 'iTime'),
                        html.Div(className = 'q-value', id='iTime'),
                        html.Label(className = 'unit', children = 'sec')
                    ]),
                ]),
            ]),
        ]),

        ### Right-Icons ###

        html.Div(id = 'right-icons', className = 'column right-icons', children = [

            # Patient Parameters #

            html.Div(className = 'parameters-title', children = [
                html.H2(children = 'Input patient parameters'),
            ]),
            
            html.Div(className = 'patient-parameters', children = [
                
                # Gender

                html.Div(className = 'patient-gender', children = [
                    dcc.Tabs(
                        id = "gender", 
                        value = 'Man',
                        children = [
                            dcc.Tab(label = 'Man', value = 'Man'),
                            dcc.Tab(label = 'Woman', value = 'Woman'),
                        ], 
                        persistence = True,
                    ),
                ]),

                # Height

                html.Div(className = 'patient-height', children = [
                    html.Div(className = 'height-output', children = [
                        html.H3(id = 'height',)
                    ]),
                    dcc.Slider(
                        id = 'Height', 
                        className = 'slider-element',
                        min = 130, 
                        max = 210, 
                        value = 170,
                        persistence = True,
                        marks = {
                            130: '130',
                            150: '150',
                            170: '170',
                            190: '190',
                            210: '210',
                        },
                    ),
                ])
            ]),

            # Controlled Parameters #
            
            html.Div(className = 'parameters-title', children = [
                html.H2(children = 'Controlled Parameters'),
            ]),
            
            # Variable Parameter 1

            html.Div(className = 'parameter-control-div', children = [
                html.Div(className = 'parameter-output', children = [
                    html.Div(className = 'parameter-name', children = [
                        html.H3('RR'),
                    ]),
                    html.Div(className = 'parameter-value', id = 'freq_out'),
                    html.Div(className = 'parameter-unit', children = [
                        html.Label('bpm'),
                    ]),
                ]),
                dcc.Slider(
                    id = 'Frequency', 
                    className = 'slider-element',
                    value = 15, 
                    min = 10, 
                    max = 30,
                    persistence = True,
                    marks = {
                        10: '10',
                        15: '15',
                        20: '20',
                        25: '25',
                        30: '30'
                    },
                ),
            ]),

            # Variable Parameter 2

            html.Div(className = 'parameter-control-div', children = [
                html.Div(className = 'parameter-output', children = [
                    html.Div(className = 'parameter-name', children = [
                        html.H3('I:E'),
                    ]),
                    html.Div(className = 'parameter-value', id = 'ie_out'),
                    html.Div(className = 'parameter-unit', children = [
                        html.Label('ratio'),
                    ]),
                ]),
                dcc.Slider(
                    id = 'ie', 
                    className = 'slider-element',
                    min = 0,
                    max = 4, 
                    step = 0.1,
                    persistence = True,
                    marks = {
                        0: '1:1',
                        1: '1:2',
                        2: '1:3',
                        3: '1:4',
                        4: '1:5',
                    }, 
                    value = 1, 
                ),
            ]),

            # Variable Parameter 3

            html.Div(className = 'parameter-control-div', children = [
                    html.Div(className = 'parameter-output', children = [
                        html.Div(className = 'parameter-name', children = [
                            html.H3('Tpause'),
                        ]),
                        html.Div(className = 'parameter-value', id = 'tpause'),
                        html.Div(className = 'parameter-unit', children = [
                            html.Label('s'),
                        ]),
                    ]),
                    dcc.Slider(
                        id = 'Pause', 
                        className = 'slider-element',
                        value = 0, 
                        min = 0, 
                        max = 0.6,
                        step = 0.1,
                        persistence = True,
                        marks = {
                            0: '0',
                            0.2: '0.2',
                            0.4: '0.4',
                            0.6: '0.6',
                        },
                    ),
                ]),

            # Variable Parameter 4

            html.Div(className = 'parameter-control-div', children = [
                html.Div(className = 'parameter-output', children = [
                    html.Div(className = 'parameter-name', children = [
                        html.H3('TV/IBW'),
                    ]),
                    html.Div(className = 'parameter-value', id = 'tv_out'),
                    html.Div(className = 'parameter-unit', children = [
                        html.Label('mL/kg'),
                    ]),
                ]),
                dcc.Slider(
                    id = 'TV', 
                    className = 'slider-element',
                    value = 8, 
                    min = 5, 
                    max = 15,
                    step = 0.2,
                    persistence = True,
                    marks = {
                        5: '5',
                        7: '7',
                        9: '9',
                        11: '11',
                        13: '13',
                        15: '15'
                    },
                ),
            ]),

            # Alternate Header

            html.Div(id = 'header2', children = [
                html.H1('SM.Pi | VC - AC'),
            ]),
        ]),
    ]),

    ### FOOTER ###

    html.Div(id = 'footer', className = 'footer', children = [
        html.H3(children = 'This is the footer'),
        html.P('SM.PI Interface - Developed April 2020 | Sarrey, Thevenet, Muller'),
    ]),

    ### ONOFF BUTTON ###

    html.Div(className = 'onoff', children = [
        dcc.Tabs(
            id = "onoff", 
            value = 'Off',
            children = [
                dcc.Tab(label = 'On', value = 'On'),
                dcc.Tab(label = 'Off', value = 'Off'),
            ], 
            persistence = True,
        ),
    ]),
    
    ### MINI TERMINAL - GCODE OUTPUT ###

    html.Div(className = 'mini-terminal', id = 'mini-terminal', children = [
        html.Div(className = 'mini-terminal1', id = 'mini-terminal1'),
        html.Div(className = 'mini-terminal2', id = 'mini-terminal2'),
    ]),

    ### INVISIBLE PLACEHOLDERS ###

    dcc.Interval(
        id = 'graph-update',
        interval = 10000,
        n_intervals = 0,
    ),

    html.Div(id = 'flowplaceholder', children = []),

    html.Div(id = 'pressureplaceholder', children = []),

])


### --- CALLBACKS --- ###


# Patient Parameters #

app.clientside_callback(
    """
    function(Height) {
        return 'Height: '+Height+' cm';
    }
    """,
    Output('height', 'children'),
    [Input('Height', 'value')]
)

# Controlled Parameters #

app.clientside_callback(
    """
    function(Frequency) {
        return Frequency;
    }
    """,
    Output('freq_out', 'children'),
    [Input('Frequency', 'value')]
)

app.clientside_callback(
    """
    function(ie) {
        return '1 : '+ (ie+1).toFixed(1);
    }
    """,
    Output('ie_out', 'children'),
    [Input('ie', 'value')]
)

app.clientside_callback(
    """
    function(TV) {
        return TV;
    }
    """,
    Output('tv_out', 'children'),
    [Input('TV', 'value')]
)

app.clientside_callback(
    """
    function(Pause) {
        return Pause;
    }
    """,
    Output('tpause', 'children'),
    [Input('Pause', 'value')]
)

# Constants #

app.clientside_callback(
    """
    function(Height, gender) {
        if (gender == 'Woman') {
            return (45.5+0.91*(Height-152.4)).toFixed(1)
        } else{
            return (50+0.91*(Height-152.4)).toFixed(1)
        }
    }
    """,
    Output('ibw', 'children'),
    [Input('Height', 'value'), Input('gender', 'value')]
)

app.clientside_callback(
    """
    function(Height, gender, TV) {
        if (gender == 'Woman') {
            return (TV*(45.5+0.91*(Height-152.4))).toFixed(0)
        } else{
            return (TV*(50+0.91*(Height-152.4))).toFixed(0)
        }
    }
    """,
    Output('tv', 'children'),
    [Input('Height', 'value'), Input('gender', 'value'), Input('TV', 'value')]
)

app.clientside_callback(
    """
    function(tv, Frequency) {
        return (tv*Frequency*0.001).toFixed(1);
    }
    """,
    Output('mv', 'children'),
    [ Input('tv', 'children'), Input('Frequency', 'value')]
)

app.clientside_callback(
    """
    function(ie, Frequency) {
        return ((60/Frequency)*(1/(2+ie))).toFixed(3);
    }
    """,
    Output('iTime', 'children'),
    [Input('ie', 'value'), Input('Frequency', 'value')]
)

# Callback Frequency #

app.clientside_callback(
    """
    function(frequency) {
        var interval_value = 60000/frequency;
        return interval_value
    }
    """,
    Output('graph-update', 'interval'),
    [Input('Frequency', 'value')]
)

# Flow Data #

app.clientside_callback(
    """
    function(onoff, Frequency, TV, ie, Height, gender) {
        let flow_x = [];
        for (var x = 0; x < 600/Frequency; x++) {
            flow_x.push(x);
        }
        let flow = [];
        if (onoff == 'On') {
            flow_x.forEach(function (item, index) {
                if ((item/10)%(60/Frequency) <= (1/(2+ie))*(60/Frequency)) {
                    if (gender == 'Woman') {
                        flow.push(0.06*((TV*(45.5+0.91*(Height-152.4)))/((60/Frequency)*(1/(2+ie)))));
                    } else {
                        flow.push(0.06*((TV*(50+0.91*(Height-152.4)))/((60/Frequency)*(1/(2+ie)))));
                    };
                } else {
                    flow.push(0);
                };
            });
        } else {
            flow_x.forEach(function (item, index) {
                flow.push(0);
            });
        };
        return flow;
    }
    """,
    Output('flowplaceholder', 'children'),
    [Input('onoff', 'value'), Input('Frequency', 'value'), Input('TV', 'value'), Input('ie', 'value'), Input('Height', 'value'),  Input('gender', 'value')]
)

# Graphs #

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='graphs'
    ),
    [Output('live-graph1', 'figure'), 
    Output('live-graph2', 'figure')
    ],
    inputs=[Input('graph-update', 'n_intervals')], 
    state = [State('flowplaceholder', 'children'), 
    State('pressureplaceholder', 'children'), 
    State('onoff', 'value')],
)

# Calibration #

def vol_to_turns(v):
    # convert tidal volume wanted to number of turns, change based on dimensions
    return v

# Mini-terminal, Gcode Generator And Pressure Data Retriever #

T = 0
last_2 = [(0, 'initializing;'), (0, 'initializing;')]

@app.callback([Output('mini-terminal1', 'children'),
            Output('mini-terminal2', 'children'),
            Output('pressureplaceholder', 'children')
            ],
            inputs=[Input('graph-update', 'n_intervals')], 
            state = [State('tv', 'children'), 
            State('iTime', 'children'), 
            State('Frequency', 'value'), 
            State('Pause', 'value'), 
            State('onoff', 'value')])
def run(input_data, tv, iTime, freq_out, tpause, onoff): 
    
    # global variables
    global T, last_2
    
    # generate gcode
    if onoff == 'On':
        
        if time.time()-T > 0.8*(60/freq_out) and tv is not None and iTime is not None:
            turns = round(vol_to_turns(float(tv)/1000), 4)
            itime = round(float(iTime), 3)
            sleep = tpause
            gcode = 'V{}T{}S{};'.format(turns, itime, sleep)
            t_1 = round(time.time() - t_0, 2)
            print(t_1)
            print(gcode)
            ser.write(str.encode(gcode))
            T = time.time()
            last_2[0] = last_2[1]
            last_2[1] = (t_1, gcode)
        else:
            print('Not updated')

    mini_terminal_output1 = ['{0:.2f}: {1}'.format(last_2[0][0]%60, last_2[0][1])]
    mini_terminal_output2 = ['{0:.2f}: {1}'.format(last_2[1][0]%60, last_2[1][1])]

    
    # retrieve pressure values
    # pressure_code = ser.read()
    # pressure_code = generate_pressure(20)
    

    return mini_terminal_output1, mini_terminal_output2, None # pressure_code


### --- EXECUTION --- ###


if __name__ == '_main_':
    app.run_server(debug=False)
