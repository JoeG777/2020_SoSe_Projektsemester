let mouseDown = false;

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
    let quelle1 = "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=1579970090373&to=1582171278843&panelId=2";
    let quelle2 = "http://localhost:3000/d-solo/SoFiK5XZz/kondensator-and-verdampfer-2w?orgId=1&from=1579970090373&to=1582171278843&panelId=3";
    switch (index) {
        case 1:
        document.querySelector('.grafana-frame').src = quelle1;
        document.querySelector('.dropbtn').innerHTML = "Dashboard 1";
        break;
        case 2:
        document.querySelector('.grafana-frame').src = quelle2;
        document.querySelector('.dropbtn').innerHTML = "Dashboard 2";
        break;
    }
}

