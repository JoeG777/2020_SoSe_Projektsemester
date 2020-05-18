/*let predictionUnits = [{"independent": ["outdoor"],
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
                        ]*/
var edgesPredictionCalcValues = {}
var cy = null;

$(document).ready(fetchModelData())

function fetchModelData() {
    jQuery.when(
        jQuery.getJSON('get_model_data')
    ).done(function (json) {
        init(json)
    })
}


function init(data) {
    let predictionUnits = data.prediction_units //createElementArray(predictionUnits);

    cy = cytoscape({

        container: document.getElementById('cy'), // container to render in

        elements: createElementArray(predictionUnits),
        style: [ // the stylesheet for the graph
          {
            selector: 'node',
            style: {
              'background-color': '#666',
              'label': 'data(id)'
            }
          },

          {
            selector: 'edge',
            style: {
              'width': 3,
              'line-color': '#ccc',
              'target-arrow-color': '#ccc',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier'
            }
          }
        ],

        layout: {
          name: 'cose',

        }

      });


  cy.on('mouseover', 'edge', function(evt)  {
      let eventId = evt.target.id();

      let values = edgesPredictionCalcValues[eventId];

      $('#parameter_wrapper').offset({
                left:  evt.pageX,
                top:   evt.pageY
      });
      console.log(values);
  });
}

function onEdgeHover(evt) {
    let eventId = evt.target.id();
    let value = edgesPredictionCalcValues[eventId];


}
function createElementArray(predictionUnits) {
    let elements = [];
    let predictionUnitId = 10;

    for (let i = 0; i < predictionUnits.length; i++) {
        let currentUnit = predictionUnits[i];

        let dependent = predictionUnits[i]['dependent'];
        let independent = predictionUnits[i]['independent'];

        for (let j = 0; j < independent.length; j++) {
            let currentNode = {
                'data': {'id': independent[j]},
            }

            if (!elements.includes(currentNode)) {
                elements.push(currentNode);
            }
        }

        for (let j = 0; j < dependent.length; j++) {
            let currentNode = {
                'data': {'id': dependent[j]},
            }

            if (!elements.includes(currentNode)) {
                elements.push(currentNode);
            }

            for (let k = 0; k < independent.length; k++) {
                let node = elements.find(n => n['data']['id'] == independent[k])

                let id = predictionUnitId + '-' + node['data']['id'] + independent[j];
                let linkNode = {
                    'data': {
                        'id': id,
                        'source': node['data']['id'],
                        'target': dependent[j]
                    }
                }
                edgesPredictionCalcValues[id] = 'yalla es geht';

                elements.push(linkNode);
            }

            // create nodes and create link or create link only
        }

        predictionUnitId += 10;
    }

    return elements;

}

$(document).on('mousemove', function(e){

});

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
//test_sample_size.innerHTML = predictionUnits[0]['test_sample_size']
//explained_variance_score.innerHTML = predictionUnits[0]['explained_variance_score']
//max_error.innerHTML = predictionUnits[0]['max_error']
//mean_absolute_error.innerHTML = predictionUnits[0]['mean_absolute_error']
//mean_squared_error.innerHTML = predictionUnits[0]['mean_squared_error']
//median_absolute_error.innerHTML = predictionUnits[0]['median_absolute_error']
//r2_score.innerHTML = predictionUnits[0]['r2_score']