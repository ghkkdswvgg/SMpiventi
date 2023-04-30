let L = 0;
let X = [];
for (let x = 0; x < 10*20; x++) {
    X.push(x);
};
let Y = [];
let Y2 = [];
X.forEach(function (item, index) {
    Y.push(0);
    Y2.push(0);
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        graphs: function(input_data, flow_data, pressure_code, onoff) {
            
            let trace1 = {
                x: X,
                y: Y,
                name : 'Flow',
                mode : 'none',
                fill : 'tonexty',
                fillcolor: 'turquoise',
            };

            let data1 = [trace1];

            let layout1 = {
                xaxis : {range: [0, (X.length)-1], tickmode:'array', gridcolor: '#555'},
                yaxis : {range: [0, 150], gridcolor: '#555'},
                font:{'color':'white'},
                autosize: true,
                showlegend: false,
                margin: {
                    b: '30',
                    t: '10',
                    l: '30',
                    r: '5',
                    pad: '5',
                }
            }

            Plotly.plot('graph1box', data1, layout1, {scrollZoom: true, staticPlot: true, responsive: true});
            
            let h = flow_data.length;
            for (let j = 0; j < (Y.length - h); j++) {
                Y[j] = Y[j+h];
            };
            for (let i = 0; i < h; i++) {
                Y[i + Y.length - h] = flow_data[i]
            };

        },
    },
});
