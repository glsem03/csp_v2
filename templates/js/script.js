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

    $('#avatar__btn').click(function () {
        $('#avatar').click();
    });


    const fileIn = document.getElementById('avatar'),
        fileOut = document.getElementById('avatar-result');

    const readUrl = event => {
        if (event.files && event.files[0]) {
            let reader = new FileReader();
            reader.onload = event => fileOut.src = event.target.result;
            reader.readAsDataURL(event.files[0])
        }
    }

    fileIn.onchange = function () {
        readUrl(this);
    };


});