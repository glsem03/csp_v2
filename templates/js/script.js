$(document).ready(function () {
    $('.header__burger').click(function (event) {
        $('.header__burger, .header__links, .header__profile').toggleClass('burger__active');
        $('body').toggleClass('lock');
    });


    function hover(element) {
        element.setAttribute('src', 'img/logo_white.png');
    }

    function unhover(element) {
        element.setAttribute('src', 'img/login_black.png');
    }





});