
// scatter plot for query results
// from https://plot.ly/javascript/getting-started/#hello-world-example
// and https://plot.ly/javascript/line-charts/
//
function scatterPlot(neural, behavioral) {
    var trace1 = {
          x: neural,
          y: behavioral,
          mode: 'markers'
    };
    var data = [ trace1 ];

    var layout = {
        title: 'Neural vs. Behavioral',
        xaxis: {
            title: 'Neural'
        },
        yaxis: {
            title: 'Behavioral'
        }
    };

    Plotly.newPlot('scatter_plot', data, layout);

    /*
    TESTER = document.getElementById('scatter_plot');
    Plotly.plot( TESTER, [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16] }], {
    margin: { t: 0 } } );
    */
}


// draw map
// from https://developers.google.com/maps/documentation/javascript/examples/polyline-simple

function initMap() {
    // convert from python to javascript array
    //
    var coords = [];
    var bounds  = new google.maps.LatLngBounds(); // to auto zoom / pan map
    for (var i = 0; i < loc.length; i++) {
        coords.push({lat: loc[i][0], lng: loc[i][1]})
        bounds.extend(new google.maps.LatLng(loc[i][0], loc[i][1]));
    }

    // global map
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: {lat: 0, lng: -180},
      mapTypeId: 'terrain'
    });
    map.fitBounds(bounds);
    map.panToBounds(bounds);
   
    /*
    var flightPlanCoordinates = [
      {lat: 37.772, lng: -122.214},
      {lat: 21.291, lng: -157.821},
      {lat: -18.142, lng: 178.431},
      {lat: -27.467, lng: 153.027}
    ];
    */
    var path = new google.maps.Polyline({
      path: coords,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    
    path.setMap(map);
}


function plotPath(loc, signal) {
    var coords = [];
    var bounds = new google.maps.LatLngBounds(); // to auto zoom / pan map
    var min = 1000000;
    var max = -1000000;
    var nan = -1000000;
    for (var i = 0; i < loc.length; i++) {
        coords.push({lat: loc[i][0], lng: loc[i][1]})
        bounds.extend(new google.maps.LatLng(loc[i][0], loc[i][1]));

        if (i < signal.length) {
            if (signal[i] != nan) { // TODO hack b/c NaN cannot be jsonified
                min = Math.min(min, signal[i]);
                max = Math.max(max, signal[i]);
            }
        }
    }
    map.fitBounds(bounds);
    map.panToBounds(bounds);

    for (var i = 0; i + 1 < loc.length; i++) {
        if (signal[i] == nan) {
            continue;
        }
        var color = 'rgb(' + (Math.floor(256 * (signal[i] - min) / (max - min))).toString() + ',0,0)';
        var path = new google.maps.Polyline({
            path: [coords[i], coords[i+1]],
            geodesic: true,
            strokeColor: color,
            strokeOpacity: 1.0,
            strokeWeight: 4,
            map: map
        });
    }
    
    path.setMap(map);
}




// plot EEG data
// from https://canvasjs.com/html5-javascript-dynamic-chart/
// also read up on http://developer.choosemuse.com/tools/available-data#DRLRefData
//
var neural_dps = [[],[],[],[],[],[]]; // dataPoints
var neural_mt = []; // millisecond timestamps (for sync w/ behavioral data)
var neural_chart = new CanvasJS.Chart("neural_chart_container", {
    title :{
        text: "Absolute " + $('#tab_neural_chart').val() + " power"
    },
    axisY: {
        includeZero: false,
        title: "Bels"
    },      
    axisX: {
        valueFormatString: "MM/DD/YY hh:mm:ss"
    },
    data: [{
        name: "EEG1",
        type: "line",
        showInLegend: true,
        dataPoints: neural_dps[0]
    }, {
        name: "EEG2",
        type: "line",
        showInLegend: true,
        dataPoints: neural_dps[1]
    }, {
        name: "EEG3",
        type: "line",
        showInLegend: true,
        dataPoints: neural_dps[2]
    }, {
        name: "EEG4",
        type: "line",
        showInLegend: true,
        dataPoints: neural_dps[3]
    }]
});
var neural_fields = ['eeg1', 'eeg2', 'eeg3', 'eeg4'];

var behavioral_dps = [[],[],[]]; // dataPoints
var behavioral_mt = []; // millisecond timestamps (for sync w/ neural data)
var behavioral_chart = new CanvasJS.Chart("behavioral_chart_container", {
    title :{
        text: "" + $('#tab_behavioral_chart').val() + ""
    },
    axisY: {
        includeZero: false,
        title: "milli-G"
    },      
    axisX: {
        valueFormatString: "MM/DD/YY hh:mm:ss"
    },
    data: [{
        name: "x",
        type: "line",
        showInLegend: true,
        dataPoints: behavioral_dps[0]
    }, {
        name: "y",
        type: "line",
        showInLegend: true,
        dataPoints: behavioral_dps[1]
    }, {
        name: "z",
        type: "line",
        showInLegend: true,
        dataPoints: behavioral_dps[2]
    }]
});
var behavioral_fields = ['x', 'y', 'z'];



var eegUpdateInterval = 1000;
//eegUpdateInterval *= 1000;
var last_id = -1;
var dataLength = 500;
var refreshed = false;

// get latest EEG data
//
var getEEG = function () {

    // TODO breaks if post request is sent before previous one is received
    // NOT thread-safe
    //
    $.post(get_eeg_url, $('form#chart_form').serialize(), function() {}, 'json')
    .done(function(data) {
        console.log(data);

        if (refreshed) {
            refreshed = false;
            // if we refreshed -> these data are irrelevant
            return;
        }

        // Neural 
        // go in reverse order b/c ORDER BY DESC
        //
        for (var j = 0; j < neural_fields.length; j++) {
            var key = neural_fields[j];
            for (var i = data[key].length - 1; i >= 0; i--) {
                neural_dps[j].push({
                    x: new Date(data['neural_mt'][i]),
                    y: data[key][i],
                });
                last_id = Math.max(last_id, data['neural_id'][i]);
            }
        }
        for (var i = data['neural_mt'].length - 1; i >= 0; i--) {
            neural_mt.push(data['neural_mt'][i]);
        }

        // trim arrays
        for (var j = 0; j < neural_dps.length; j++) {
            while (neural_dps[j].length > dataLength) {
                neural_dps[j].shift();
            }
        }
        while (neural_mt.length > dataLength) {
            neural_mt.shift();
        }

        // update last neural id
        $('#last_id_hack').val(last_id);

        // render chart
        neural_chart.render();

        // Behavioral
        // go in reverse order b/c ORDER BY DESC
        //
        for (var j = 0; j < behavioral_fields.length; j++) {
            var key = behavioral_fields[j];
            for (var i = data[key].length - 1; i >= 0; i--) {
                behavioral_dps[j].push({
                    x: new Date(data['behavioral_mt'][i]),
                    y: data[key][i]
                });
            }
        }
        for (var i = data['behavioral_mt'].length - 1; i >= 0; i--) {
            behavioral_mt.push(data['behavioral_mt'][i]);
        }

        // trim arrays, according to timestamps
        while (behavioral_mt.length > 0 && behavioral_mt[0] <= neural_mt[0]) {
            for (var j = 0; j < behavioral_dps.length; j++) {
                behavioral_dps[j].shift();
            }
            behavioral_mt.shift();
        }

        // render chart
        behavioral_chart.render();
    })
    .fail(function(xhr, status, error) {
        console.log('get_eeg error');
        console.log(error);
    })
    .always(function() {
        if ($('#live_chart').prop('checked')) {
            setTimeout(getEEG, eegUpdateInterval); // do it this way rather than setInterval to avoid getting overlapping requests
        }
    });
}


function refreshCharts() { 
    for (var j = 0; j < neural_dps.length; j++) {
        neural_dps[j].length = 0;  // important -- clear in place; address needs to stay the same
    }
    neural_mt.length = 0;
    for (var j = 0; j < behavioral_dps.length; j++) {
        behavioral_dps[j].length = 0;  // important -- clear in place; address needs to stay the same
    }
    behavioral_mt.length = 0;
    neural_chart.options.title.text = "Absolute " + $('#tab_neural_chart').val() + " power"
    behavioral_chart.options.title.text = "Absolute " + $('#tab_behavioral_chart').val() + " power"
    last_id = -1;
    $('#last_id_hack').val(last_id);
    refreshed = true;
}

// change neural_chart frequency range 
//
$('select#tab_neural_chart').change( function() {
    refreshCharts();
});
$('select#tab_behavioral_chart').change( function() {
    refreshCharts();
});





// handle submit for correlate form (Run button)
// from https://stackoverflow.com/questions/1200266/submit-a-form-using-jquery
//
$('input#submit_corr').click( function() {

    $('#submit_corr_spinner').show();
    $('#submit_corr').hide();
    $.post(correlate_url, $('form#correlate').serialize(), function() {}, 'json')
    .done(function(data) {
        console.log(data);
        var r = data['r'];
        var p = data['p'];
        $('#corr_result').html("r = " + r.toString() + ", p = " + p.toString());
        var neural = data['ret1']
        var behavioral = data['ret2']
        scatterPlot(neural, behavioral);
    })
    .fail(function(xhr, status, error) {
        $('#corr_result').html("ERROR");
        console.log(error);
    })
    .always(function() {
        $('#save_result').html("");
        $('#submit_corr_spinner').hide();
        $('#submit_corr').show();
    });
});

// handle submit for location plotting (Locate button)
//
$('input#submit_loc').click( function() {

    $('#submit_loc_spinner').show();
    $('#submit_loc').hide();
    $.post(locate_url, $('form#correlate').serialize(), function() {}, 'json')
    .done(function(data) {
        console.log(data);

        var loc = data['loc']
        var signal = data['signal']
        plotPath(loc, signal);
    })
    .fail(function(xhr, status, error) {
        //$('#corr_result').html("ERROR");
        console.log(error);
    })
    .always(function() {
        $('#submit_loc_spinner').hide();
        $('#submit_loc').show();
    });
});

// handle submit for save query
//
$('input#save_query').click( function() {

    $.post(save_query_url, $('form#correlate').serialize(), function() {}, 'json')
    .done(function(data) {
        console.log(data);
        $('#save_result').html("Saved!");
    })
    .fail(function(xhr, status, error) {
        $('#save_result').html("ERROR!");
        console.log(error);
    })
});

// handle load query
//
$('select#queries').change( function() {

    if ($('#queries').val() != '0') {
        $.get(load_query_url, { id: $('#queries').val() }, function(data) {
            console.log(data);
            for (var name in data) {
                if (name != 'queries') {
                    $('#' + name).val(data[name]);
                }
            }
            },
            'json' // I expect a JSON response
        );
    } else {
        // new query -> clear form
        $('form#correlate').trigger('reset');
    }
});




hsi = [0, 0, 0, 0];
hsiUpdateInterval = 1000;
//hsiUpdateInterval *= 1000;
hsiLastMt = -1;

function setupHSICanvas() {
    var img = document.getElementById("electrodes");

    var canvas = document.getElementById('electrodes_canvas');
    canvas.style.position = "absolute";
    canvas.style.left = img.offsetLeft + "px";
    canvas.style.top = img.offsetTop + "px";
    canvas.style.width = img.width + "px";
    canvas.style.height = img.height + "px";
}

function DrawHSI(){
    var canvas = document.getElementById('electrodes_canvas');

    var centers = [{
        x: canvas.width * 0.1,
        y: canvas.height * 0.65
    }, {
        x: canvas.width * 0.35,
        y: canvas.height * 0.25
    }, {
        x: canvas.width * 0.65,
        y: canvas.height * 0.25
    }, {
        x: canvas.width * 0.9,
        y: canvas.height * 0.65
    }];

    fillStyle = ["grey", "green", "yellow", "red", "red"];
    strokeStyle = ["#222222", "#003300", "333300", "330000", "330000"];

    var context = canvas.getContext('2d');
    var radius = 8;

    for (var i = 0; i < centers.length; i++) {
        var centerX = centers[i].x; 
        var centerY = centers[i].y;

        context.beginPath();
        context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
        context.fillStyle = fillStyle[hsi[i]];
        context.fill();
        context.lineWidth = 0;
        context.strokeStyle = strokeStyle[hsi[i]];
        context.stroke();    

        context.fillStyle = 'black';
        context.textAlign = 'center';
        context.fillText((i+1).toString(), centerX, centerY + 3);
    }
}


function formatDate(date) {
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();
    var hour = date.getHours();
    var mins = date.getMinutes();
    var secs = date.getSeconds();
    

   // return day + ' ' + monthNames[monthIndex] + ' ' + year;
    return (monthIndex + 1) + '/' + day + '/' + year + ' ' + hour + ':' + mins + ':' + secs;
}


var getHSI = function () {

    $.post(get_hsi_url, {}, function() {}, 'json')
    .done(function(data) {
        console.log(data);

        hsi = data[0];
        hsiLastMt = data[0][4]; 

        var hsiLast = new Date(hsiLastMt);
        var diff = Date.now() - hsiLast.getTime(); // in milliseconds
        if (diff > 10000) {
            $('#status').text('Offline since ' + formatDate(hsiLast));
            $('#status').css('color', 'red');
        } else {
            $('#status').text('Online');
            $('#status').css('color', 'green');
        }

        DrawHSI();
    })
    .fail(function(xhr, status, error) {
        console.log('get_hsi error');
        console.log(error);
    })
    .always(function() {
        if ($('#live_chart').prop('checked')) {
            setTimeout(getHSI, hsiUpdateInterval); // do it this way rather than setInterval to avoid getting overlapping requests
        }
    });
}


// setup charts and stuff on window load
//
window.onload = function () {
    getEEG();

    setupHSICanvas();
    getHSI();
}


$('#live_chart').change(function() {
    if ($('#live_chart').prop('checked')) {
        getEEG();
        getHSI();
    }
});
