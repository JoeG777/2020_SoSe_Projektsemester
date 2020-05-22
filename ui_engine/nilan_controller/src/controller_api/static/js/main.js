let mouseDown = false;

$(document).ready(function(){
    jQuery('#datetimepicker').datetimepicker();
});

/* Grafana-Dashboards */

let dashboardTimestamps = {
    "start_date": "",
    "end_date": ""
};

let dashboards = {
    "dashboard_1": "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=" + dashboardTimestamps["start_date"] + "&to=" + dashboardTimestamps["end_date"] + "&panelId=2",
    "dashboard_2": "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=" + dashboardTimestamps["start_date"] + "&to=" + dashboardTimestamps["end_date"] + "&panelId=3"
};

document.getElementById('grafana_frame').src = dashboards["dashboard_1"];

let activeDashboard = 1;

set_initial_date();
refreshTimePeriod();

/* Dropdown Menu */
document.querySelector('.heading').innerHTML = "CONTROL PANEL";

function press_dropdown() {
    document.querySelector('.dropdown_arrow').classList.toggle('active');
    document.getElementById('dropdown_option_1').classList.toggle('active');
    document.getElementById('dropdown_option_2').classList.toggle('active');
}

function option_pressed(option) {
    if (option == 1) {
        document.getElementById('content').classList.add('active');
        document.getElementById('cy').classList.remove('active');
        document.getElementById('dashboard_dropdown').classList.add('active');
        document.getElementById('btn_wrapper').classList.add('active');
        press_dropdown()
        document.querySelector('.heading').innerHTML = "CONTROL PANEL";
    } else {
        document.getElementById('content').classList.remove('active');
        document.getElementById('cy').classList.add('active');
        document.getElementById('dashboard_dropdown').classList.remove('active');
        document.getElementById('btn_wrapper').classList.remove('active');
        press_dropdown()
        document.querySelector('.heading').innerHTML = "CURRENT MODEL";
    }
}

/* Variablen für Buttons */

let btnAktualisieren = document.getElementById('aktualisieren');
let btnAnwenden = document.getElementById('anwenden');
let einstellungenAktualisiert = false;
let werteGeaendert = false;

/******/

setInititalPositionRaumtemp();
setInititalPositionZuluft();
setInititalPositionAbluft();
setInititalPositionBetriebsmodus();

let raumtemperaturSlider = document.getElementById('raumtemperaturSlider');
let zuluftSlider = document.getElementById('lüfterZuluftSlider');
let abluftSlider = document.getElementById('lüfterAbluftSlider');
let betriebsmodusSlider = document.getElementById('betriebsmodusSlider');

raumtemperaturSlider.addEventListener('mousedown', function () {
    mouseDown = true;
    document.querySelector('.currentValue1').classList.add('bigger');
});
raumtemperaturSlider.addEventListener('mouseup', function () {
    mouseDown = false;
    document.querySelector('.currentValue1').classList.remove('bigger');
});
zuluftSlider.addEventListener('mousedown', function () {
    mouseDown = true;
    document.querySelector('.currentValue2').classList.add('bigger');
});
zuluftSlider.addEventListener('mouseup', function () {
    mouseDown = false;
    document.querySelector('.currentValue2').classList.remove('bigger');
});
abluftSlider.addEventListener('mousedown', function () {
    mouseDown = true;
    document.querySelector('.currentValue3').classList.add('bigger');
});
abluftSlider.addEventListener('mouseup', function () {
    mouseDown = false;
    document.querySelector('.currentValue3').classList.remove('bigger');
});
betriebsmodusSlider.addEventListener('mousedown', function () {
    mouseDown = true;
    document.querySelector('.currentValue4').classList.add('bigger');
});
betriebsmodusSlider.addEventListener('mouseup', function () {
    mouseDown = false;
    document.querySelector('.currentValue4').classList.remove('bigger');
});
raumtemperaturSlider.addEventListener('mousemove', function(event) {
    update(event, 'raumtemperaturSlider', '.current1', '.raumtempLow', '.raumtempHigh')
});
lüfterZuluftSlider.addEventListener('mousemove', function(event) {
    update(event, 'lüfterZuluftSlider', '.current2', '.zuluftLow', '.zuluftHigh')
});
abluftSlider.addEventListener('mousemove', function(event) {
    update(event, 'lüfterAbluftSlider', '.current3', '.abluftLow', '.abluftHigh');
});
betriebsmodusSlider.addEventListener('mousemove', function(event) {
    update(event, 'betriebsmodusSlider', '.current4', '.betriebsmodusLow', '.betriebsmodusHigh')
});

function update (event, slider, span, low, high) {
    if (mouseDown) {
        if (slider == 'raumtemperaturSlider') {
            let raumtemperatur = document.getElementById(slider).value
            if (raumtemperatur < 1900) {
                document.querySelector(low).classList.add('disable')
            }
            if (raumtemperatur > 1900) {
                document.querySelector(low).classList.remove('disable')
            }
            if (raumtemperatur < 2300) {
                document.querySelector(high).classList.remove('disable')
            }
            if (raumtemperatur > 2300) {
                document.querySelector(high).classList.add('disable')
            }
            let verhältnis = (raumtemperatur-1800) / 600
            let object = document.querySelector(span);
            let marginLeft = document.getElementById(slider).offsetLeft
            let left = 465 * verhältnis;
            object.style.left = left + marginLeft;
            let raumtemperaturValue = Math.round(raumtemperatur / 100)
            document.querySelector('.currentValue1').innerHTML = raumtemperaturValue + "°C";
            werteGeaendert = true;
        }
        if (slider == 'lüfterZuluftSlider') {
            let zuluft = document.getElementById(slider).value
            if (zuluft < 1) {
                document.querySelector(low).classList.add('disable')
            }
            if (zuluft > 1) {
                document.querySelector(low).classList.remove('disable')
            }
            if (zuluft < 3) {
                document.querySelector(high).classList.remove('disable')
            }
            if (zuluft > 3) {
                document.querySelector(high).classList.add('disable')
            }
            let verhältnis = zuluft / 4;
            let object = document.querySelector(span);
            let marginLeft = document.getElementById(slider).offsetLeft;
            let left = 0;
            if (zuluft == 0) {
                left = 465 * verhältnis;
            } else {
                left = 465 * verhältnis + 13;
            }
            object.style.left = left + marginLeft;
            let zuluftValue = Math.round(zuluft)
            document.querySelector('.currentValue2').innerHTML = zuluftValue;
            werteGeaendert = true;
        }

        if (slider == 'lüfterAbluftSlider') {
            let zuluft = document.getElementById(slider).value
            if (zuluft < 1) {
                document.querySelector(low).classList.add('disable')
            }
            if (zuluft > 1) {
                document.querySelector(low).classList.remove('disable')
            }
            if (zuluft < 3) {
                document.querySelector(high).classList.remove('disable')
            }
            if (zuluft > 3) {
                document.querySelector(high).classList.add('disable')
            }
            let verhältnis = zuluft / 4
            let object = document.querySelector(span);
            let marginLeft = document.getElementById(slider).offsetLeft

            let left = 0;
            if (zuluft == 0) {
                left = 465 * verhältnis;
            } else {
                left = 465 * verhältnis + 13;
            }
            object.style.left = left + marginLeft;
            let zuluftValue = Math.round(zuluft);
            document.querySelector('.currentValue3').innerHTML = zuluftValue;
            werteGeaendert = true;
        }
        if (slider == 'betriebsmodusSlider') {

            let betriebsmodus = document.getElementById(slider).value
            if (betriebsmodus == 0) {
                document.querySelector(low).classList.add('disable')
            }
            if (betriebsmodus > 0) {
                document.querySelector(low).classList.remove('disable')
            }
            if (betriebsmodus < 2) {
                document.querySelector(high).classList.remove('disable')
            }
            if (betriebsmodus == 2) {
                document.querySelector(high).classList.add('disable')
            }
            let verhältnis = betriebsmodus / 2
            let object = document.querySelector(span);
            let marginLeft = document.getElementById(slider).offsetLeft
            let left = 465 * verhältnis;
            let kompressorValue = Math.round(betriebsmodus / 10)
            if (betriebsmodus == 0) {
                document.querySelector('.currentValue4').innerHTML = "Kühlen";
                object.style.left = left + marginLeft;
            } else if (betriebsmodus == 1) {
                document.querySelector('.currentValue4').innerHTML = "Aus";
                object.style.left = left + marginLeft;
            } else if (betriebsmodus == 2) {
                document.querySelector('.currentValue4').innerHTML = "Heizen";
                object.style.left = left + marginLeft - 20;
            }
            werteGeaendert = true;
            btnAktualisieren.classList.remove('inactive');
        }
    }
}
function setInititalPositionRaumtemp () {
    let raumtemp = document.getElementById('raumtemperaturSlider').value
    let verhältnis = (raumtemp-1800) / 600
    let object = document.querySelector('.current1');
    let marginLeft = document.getElementById('raumtemperaturSlider').offsetLeft
    let left = 465 * verhältnis;
    object.style.left = left + marginLeft;
    let raumtemperatur = Math.round(raumtemp / 100)
    document.querySelector('.currentValue1').innerHTML = raumtemperatur + "°C";
}

function setInititalPositionZuluft () {
    let zuluft = document.getElementById('lüfterZuluftSlider').value
    let verhältnis = zuluft / 4;
    let object = document.querySelector('.current2');
    let marginLeft = document.getElementById('lüfterZuluftSlider').offsetLeft
    let left = 0;
    if (zuluft == 0) {
        left = 465 * verhältnis;
    } else {
        left = 465 * verhältnis + 13;
    }
    object.style.left = left + marginLeft;
    let zuluftValue = Math.round(zuluft);
    document.querySelector('.currentValue2').innerHTML = zuluftValue;
}

function setInititalPositionAbluft () {
    let zuluft = document.getElementById('lüfterAbluftSlider').value
    let verhältnis = zuluft / 4;
    let object = document.querySelector('.current3');
    let marginLeft = document.getElementById('lüfterAbluftSlider').offsetLeft
    let left = 0;
    if (zuluft == 0) {
        left = 465 * verhältnis;
    } else {
        left = 465 * verhältnis + 13;
    }
    object.style.left = left + marginLeft;
    let zuluftValue = Math.round(zuluft);
    document.querySelector('.currentValue3').innerHTML = zuluftValue;
}

function setInititalPositionBetriebsmodus () {
    let abluft = document.getElementById('betriebsmodusSlider').value
    let verhältnis = abluft / 2
    let object = document.querySelector('.current4');
    let marginLeft = document.getElementById('betriebsmodusSlider').offsetLeft
    let left = 465 * verhältnis;
    object.style.left = left + marginLeft;
    let abluftValue = Math.round(abluft / 10)
    document.querySelector('.currentValue4').innerHTML = "Aus";
}

function dropdown (index) {
    switch (index) {
        case 1:
        document.querySelector('.grafana-frame').src = dashboards["dashboard_1"];
        document.querySelector('.dropbtn').innerHTML = "Dashboard 1";
        activeDashboard = index;
        break;
        case 2:
        document.querySelector('.grafana-frame').src = dashboards["dashboard_2"];
        document.querySelector('.dropbtn').innerHTML = "Dashboard 2";
        activeDashboard = index;
        break;
    }
}

/* Set timeperiod in Grafana */

function refreshTimePeriod () {

    var start_date = document.getElementById('start_date').value;
    var start_date_converted = start_date.substring(0,19) + ".000000000Z";
    var end_date = document.getElementById('end_date').value;
    var end_date_converted = end_date.substring(0,19) + ".000000000Z";

    var start_date_unix =  Math.round((new Date(start_date_converted)).getTime() / 1000);
    dashboardTimestamps["start_date"] = parseInt(start_date_unix + "000");

    var end_date_unix =  Math.round((new Date(end_date_converted)).getTime() / 1000);
    dashboardTimestamps["end_date"] = parseInt(end_date_unix + "000");

    dashboards["dashboard_1"] = "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=" + dashboardTimestamps["start_date"] + "&to=" + dashboardTimestamps["end_date"] + "&panelId=2";
    dashboards["dashboard_2"] = "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=" + dashboardTimestamps["start_date"] + "&to=" + dashboardTimestamps["end_date"] + "&panelId=3";

    if (activeDashboard == 1) {
        dropdown(activeDashboard);
    }

    if (activeDashboard == 2) {
        dropdown(activeDashboard);
    }

}

function set_initial_date () {

    document.getElementById('end_date').value = get_current_date();
    document.getElementById('start_date').value = get_current_date_minus_two_weeks();

}

function format_date (date_object) {

    var month = add_zero(date_object.getMonth() + 1);
    var year = date_object.getFullYear();
    var day = add_zero(date_object.getDate());

    var hour = add_zero(date_object.getHours());
    var min = add_zero(date_object.getMinutes());
    var sec = add_zero(date_object.getSeconds());

    var date = year + "-" + month + "-" + day + "T" + hour + ":" + min + ":" + sec + "Z";

    function add_zero (num) {

        if (num < 10) {
            return "0" + num;
        } else {
            return num;
        }

    }

    return date;

}

function get_current_date () {

    var date_object = new Date();
    return format_date(date_object)

}

function get_current_date_minus_two_weeks () {

    Date.prototype.AddDays = function(noOfDays) {
        this.setTime(this.getTime() + (noOfDays * (1000 * 60 * 60 * 24)));
        return this;
    }

    function get_date () {
        var dateNew = new Date();
        dateNew.AddDays(-14);
        return dateNew;
    }

    return format_date(get_date())

}

