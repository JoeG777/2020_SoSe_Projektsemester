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

    } else {

        document.getElementById('content').classList.remove('active');
        document.getElementById('cy').classList.add('active');
        document.getElementById('dashboard_dropdown').classList.remove('active');
        document.getElementById('btn_wrapper').classList.remove('active');

        press_dropdown()

    }

}
