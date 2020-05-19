let averageData = {
    "average_score": 0.5763061660139956,
    "average_explained_variance_score": 0.5763743321592572,
    "average_max_error": 8.096326490599703,
    "average_mean_absolute_error": 1.0542581697922409,
    "average_mean_squared_error": 5.5904049363090556,
    "average_median_absolute_error": 0.7699636093103956,
    "average_r2_score_avg": 0.5763637120083245
}

let predictionUnits = [{"independent": ["outdoor"],
                        "dependent": ["freshAirIntake"],
                        "test_sample_size": 0.2,
                        "explained_variance_score": 1.0,
                        "max_error": 1.2789769243681803e-13,
                        "mean_absolute_error": 2.278405095523464e-14,
                        "mean_squared_error": 8.703805249786064e-28,
                        "median_absolute_error": 1.865174681370263e-14,
                        "r2_score": 1.0
                        },
                        {"independent": ["freshAirIntake"],
                         "dependent": ["evaporator"],
                         "test_sample_size": 0.2,
                         "explained_variance_score": 0.48818420249388716,
                         "max_error": 36.83065486016068,
                         "mean_absolute_error": 1.3825711925035478,
                         "mean_squared_error": 7.071028234732214,
                         "median_absolute_error": 0.786521716559321,
                         "r2_score": 0.48817132880890124
                         },
                         {"independent": ["freshAirIntake"],
                         "dependent": ["outlet"],
                         "test_sample_size": 0.2,
                         "explained_variance_score": 0.9957086110267189,
                         "max_error": 1.0530777202267636,
                         "mean_absolute_error": 0.18703818986862245,
                         "mean_squared_error": 0.051838806393370615,
                         "median_absolute_error": 0.16520420187688956,
                         "r2_score": 0.9957079945275119
                         },
                         {"independent": ["outlet", "evaporator"],
                         "dependent": ["room"],
                         "test_sample_size": 0.2,
                         "explained_variance_score": 0.39409689392476754,
                         "max_error": 2.597899872610938,
                         "mean_absolute_error": 0.8379751101821196,
                         "mean_squared_error": 1.048255439776959,
                         "median_absolute_error": 0.7230608026499219,
                         "r2_score": 0.3940581483692188
                         },
                         {"independent": ["outdoor", "freshAirIntake"],
                         "dependent": ["inlet"],
                         "test_sample_size": 0.2,
                         "explained_variance_score": 0.005806806348559901,
                         "max_error": 67.75236956309371,
                         "mean_absolute_error": 2.7542098772958985,
                         "mean_squared_error": 16.81471032621601,
                         "median_absolute_error": 2.1694281471428667,
                         "r2_score": 0.005806104136281687
                         },
                         {"independent": ["outdoor", "freshAirIntake"],
                         "dependent": ["condenser"],
                         "test_sample_size": 0.2,
                         "explained_variance_score": 0.0019395462959949095,
                         "max_error": 85.52762483967015,
                         "mean_absolute_error": 2.979519419826366,
                         "mean_squared_error": 22.747382804899328,
                         "median_absolute_error": 2.195879102725417,
                         "r2_score": 0.0019386808175004822}
                        ]

var edgesPredictionCalcValues = {}
var cy = null;
let standardStyles = {
    'line-color': '#ffffff',
    'target-arrow-color': '#ffffff',
    'line-color-grayed-out': '#4d4b57',
    'target-arrow-color-grayed-out': '#4d4b57'
}

$(document).ready(fetchModelData())
//$(document).ready(init())

function fetchModelData() {
    jQuery.when(
        jQuery.getJSON('get_model_data')
    ).done(function (json) {
        init(json);
    })
}


function init(data) {
    $('#parameter_wrapper').hide();
    let predictionUnits = createElementArray(data.prediction_units);
    //let predictionUnitsData = predictionUnits;

    cy = cytoscape({

        container: document.getElementById('cy'), // container to render in

        elements: predictionUnits,
        style: [ // the stylesheet for the graph
          {
            selector: 'node',
            style: {
              'label': 'data(id)',
              'content': 'data(id)',
              'background-color': 'white',
              'color': 'white',
              'font-size': '24px',
              'width': '60',
              'height': '60'
            }
          },

          {
            selector: 'edge',
            style: {
              'width': '6',
              'line-color': '#ccc',
              'target-arrow-color': '#ccc',
              'target-arrow-shape': 'triangle',
              'target-arrow-shape': 'vee',
              'arrow-scale': '1',
              'curve-style': 'bezier',
            }
          },
        ],
        layout: {
          name: 'grid',
        }

      });


  cy.on('mouseover', 'edge', function(evt)  {
      let eventId = evt.target.id();

      makeEdgesGradient(eventId);

      let value = edgesPredictionCalcValues[eventId];
      $('#parameter_wrapper').show();
      $('#parameter_wrapper').offset({
                left:  evt.renderedPosition.x,
                top:   evt.renderedPosition.y
      });

   $('#test_sample_size').html(value['test_sample_size']);
   $('#explained_variance_score').html(value['explained_variance_score']);
   $('#max_error').html(value['max_error']);
   $('#mean_absolute_error').html(value['mean_absolute_error']);
   $('#mean_squared_error').html(value['mean_squared_error']);
   $('#median_absolute_error').html(value['median_absolute_error']);
   $('#r2_score').html(value['r2_score']);

  });

  /* AVERAGE PARAMETERS */

    let average_data = getAverageValues()

    $('#average_score').html(average_data['average_score']);
    $('#average_explained_variance_score').html(average_data['average_explained_variance_score']);
    $('#average_max_error').html(average_data['average_max_error']);
    $('#average_mean_absolute_error').html(average_data['average_mean_absolute_error']);
    $('#average_mean_squared_error').html(average_data['average_mean_squared_error']);
    $('#average_median_absolute_error').html(average_data['average_median_absolute_error']);
    $('#average_r2_score').html(average_data['average_r2_score']);

    cy.on('mouseout', 'edge', function(evt)  {
        $('#parameter_wrapper').hide();
        resetAllEdges();
    });
  cy.userZoomingEnabled(false);
}

function makeEdgesGradient(eventId) {
    let predictionUnitId = eventId.substring(0,2); // this should be more dynamic
    let relatedEdges = Object.keys(edgesPredictionCalcValues).filter(x => x.startsWith(predictionUnitId));
    let unrelatedEdges = Object.keys(edgesPredictionCalcValues).filter(x => !x.startsWith(predictionUnitId));


    for (let i = 0; i < relatedEdges.length; i++) {
        let currEdge = cy.$('#' + relatedEdges[i]);
        let connectedNodes = currEdge.connectedNodes();
        let firstNodeColor = connectedNodes[0].style().backgroundColor;
        let secondNodeColor = connectedNodes[1].style().backgroundColor;

        currEdge.style('line-gradient-stop-colors', firstNodeColor + ' ' + secondNodeColor);
        currEdge.style('line-fill', 'linear-gradient');
        currEdge.style('line-gradient-stop-positions', '0 100%;');
        currEdge.style('target-arrow-color', secondNodeColor);
    }
    for (let i = 0; i < unrelatedEdges.length; i++) {
        let currEdge = cy.$('#' + unrelatedEdges[i]);
        currEdge.style('line-color', standardStyles['line-color-grayed-out']);
        currEdge.style('target-arrow-color', standardStyles['target-arrow-color-grayed-out']);
    }
}

function resetAllEdges() {
    let allEdges = cy.$('edge');

    for (let i = 0; i < allEdges.length; i++) {
        allEdges[i].style('line-gradient-stop-colors', '');
        allEdges[i].style('line-fill', '');
        allEdges[i].style('line-gradient-stop-positions', '');

        allEdges[i].style('target-arrow-color', standardStyles['target-arrow-color']);
        allEdges[i].style('line-color', standardStyles['line-color']);
    }
}

function createElementArray(predictionUnits) {
    let elements = [];
    let predictionUnitId = 10;
    let elementColors = ['#E07D7D', '#90A3E3', '#EFC893', '#84D0C7', '#E0D47B', '#E3A2D9'];
    let colorCounter = 0;
    for (let i = 0; i < predictionUnits.length; i++) {
        let currentUnit = predictionUnits[i];

        let dependent = predictionUnits[i]['dependent'];
        let independent = predictionUnits[i]['independent'];

        for (let j = 0; j < independent.length; j++) {
            let currentNode = {
                'data': {'id': independent[j]},
            }

            if (!elements.includes(currentNode)) {
                if (colorCounter == elementColors.length) colorCounter = 0;
                let color = elementColors[colorCounter];
                currentNode['style'] = {}
                currentNode['style']['background-color'] = color;
                colorCounter++;
                elements.push(currentNode);
            }
        }

        for (let j = 0; j < dependent.length; j++) {
            let currentNode = {
                'data': {'id': dependent[j]},
            }

            if (!elements.includes(currentNode)) {
                if (colorCounter == elementColors.length) colorCounter = 0;
                let color = elementColors[colorCounter];
                currentNode['style'] = {}
                currentNode['style']['background-color'] = color;
                colorCounter++;
                elements.push(currentNode);
            }

            for (let k = 0; k < independent.length; k++) {
                let node = elements.find(n => n['data']['id'] == independent[k])

                let id = predictionUnitId + '-' + node['data']['id'] + dependent[j];
                let linkNode = {
                    'data': {
                        'id': id,
                        'source': node['data']['id'],
                        'target': dependent[j]
                    },
                }
                edgesPredictionCalcValues[id] = extractCalcValues(predictionUnits[i]);

                elements.push(linkNode);
            }

        }

    predictionUnitId += 10;
    }

    return elements;

}

function extractCalcValues(predictionUnit) {
    return {
         "test_sample_size": predictionUnit["test_sample_size"],
         "explained_variance_score": predictionUnit["explained_variance_score"],
         "max_error": predictionUnit["max_error"],
         "mean_absolute_error": predictionUnit["mean_absolute_error"],
         "mean_squared_error": predictionUnit["mean_squared_error"],
         "median_absolute_error": predictionUnit["median_absolute_error"],
         "r2_score": predictionUnit["r2_score"],
         "coef": predictionUnit["coef"],
         "intercept": predictionUnit["intercept"]
    }
}

function getAverageValues() {
    let data = fetchModelData()
    //let data = averageData
    return {
        "average_score": data["average_score"],
        "average_explained_variance_score": data["average_explained_variance_score"],
        "average_max_error": data["average_max_error"],
        "average_mean_absolute_error": data["average_mean_absolute_error"],
        "average_mean_squared_error": data["average_mean_squared_error"],
        "average_median_absolute_error": data["average_median_absolute_error"],
        "average_r2_score": data["average_r2_score_avg"]
    }
}

// Parameter-Viewer

let curve_name_independent = document.getElementById("curve_name_independent");
let curve_name_dependent = document.getElementById("curve_name_dependent");

let test_sample_size = document.getElementById("test_sample_size");
let explained_variance_score = document.getElementById("explained_variance_score");
let max_error = document.getElementById("max_error");
let mean_absolute_error = document.getElementById("mean_absolute_error");
let mean_squared_error = document.getElementById("mean_squared_error");
let median_absolute_error = document.getElementById("median_absolute_error");
let r2_score = document.getElementById("r2_score");
/*
//Independent Curves

for (var i = 0; i < predictionUnits[3]['independent'].length; i++) {

    var curve = document.createElement("h3");
    curve.innerHTML = predictionUnits[3]['independent'][i];
    document.querySelector(".independent_curves").appendChild(curve);

}

//Dependent Curves

for (var i = 0; i < predictionUnits[3]['dependent'].length; i++) {

    var curve = document.createElement("h3");
    curve.innerHTML = predictionUnits[3]['dependent'][i];
    document.querySelector(".dependent_curves").appendChild(curve);

}


*/
