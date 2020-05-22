var edgesPredictionCalcValues = {}
var cy = null;
let standardStyles = {
    'line-color': '#ffffff',
    'target-arrow-color': '#ffffff',
    'line-color-grayed-out': '#4d4b57',
    'target-arrow-color-grayed-out': '#4d4b57'
}

//$(document).ready(fetchModelData())

function fetchModelData() {
    $('#calc_container_wrapper').hide();
    jQuery.when(
        jQuery.getJSON('get_model_data')
    ).done(function (json) {
        $('#calc_container_wrapper').show();
        $('#curves').hide();
        $('#calc_container_curve').hide();
        init(json);
    })
}


function init(data) {
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
          rows: 3,
        }

      });


  cy.on('mouseover', 'edge', function(evt) {
      let eventId = evt.target.id();

      makeEdgesGradient(eventId);

      let value = edgesPredictionCalcValues[eventId];
      $('#curves').show();
      $('#averageHeader').hide();
      $('#calc_container_curve').show();
      $('#calc_container_average').hide();


   $('#independent_curves').append(getCurvesAsHtml(value['independent']));
   $('#dependent_curves').append(getCurvesAsHtml(value['dependent']));
   $('#test_sample_size').html(value['test_sample_size']);
   $('#explained_variance_score').html(value['explained_variance_score']);
   $('#max_error').html(value['max_error']);
   $('#mean_absolute_error').html(value['mean_absolute_error']);
   $('#mean_squared_error').html(value['mean_squared_error']);
   $('#median_absolute_error').html(value['median_absolute_error']);
   $('#r2_score').html(value['r2_score']);
   $('#function').append(generateFunction(value));

    var problems = document.getElementsByClassName('functionContainer');
   for (let i = 0; i < problems.length; i++) {
        MQ.StaticMath(problems[i]);
    }
   });

  /* AVERAGE PARAMETERS */

    let average_data = getAverageValues(data)

    $('#average_score').html(average_data['average_score']);
    $('#average_explained_variance_score').html(average_data['average_explained_variance_score']);
    $('#average_max_error').html(average_data['average_max_error']);
    $('#average_mean_absolute_error').html(average_data['average_mean_absolute_error']);
    $('#average_mean_squared_error').html(average_data['average_mean_squared_error']);
    $('#average_median_absolute_error').html(average_data['average_median_absolute_error']);
    $('#average_r2_score').html(average_data['average_r2_score']);

    cy.on('mouseout', 'edge', function(evt)  {
        $('.curveContainer').remove();
        $('.functionContainer').remove();
        $('#calc_container_curve').hide();
        $('#calc_container_average').show();
        $('#curves').hide();
        $('#averageHeader').show();
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

function generateFunction(predictionUnit) {
    let coef = predictionUnit['coef'];
    let intercept = predictionUnit['intercept'];
    let dependent = predictionUnit['dependent'];
    let independent = predictionUnit['independent'];
    let linearFunc = ''
    for (let i = 0; i < coef.length; i++) {
        linearFunc += '<div class=functionContainer>'
        for (let j = 0; j < coef[i].length; j++) {
            linearFunc += roundToTwoDec(coef[i][j]) + ' * '  + independent[j] + ' + ';
        }
        linearFunc += roundToTwoDec(intercept[i]);
        linearFunc += ' = ' + dependent[i] + '</div>';
    }
    return linearFunc;
}

function roundToTwoDec(number) {
    return Math.round((number + Number.EPSILON) * 100) / 100;
}
function extractCalcValues(predictionUnit) {
    return {
         "dependent": predictionUnit["dependent"],
         "independent": predictionUnit["independent"],
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

function getAverageValues(data) {
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

function getCurvesAsHtml(curveArray) {
    let html = '';
    for (let i = 0; i < curveArray.length; i++) {
        html += '<h3 class="curveContainer">' + curveArray[i] + '</h3>';
    }
    return html;
}
