const loginbtn = document.getElementById('loginbtn');
const menu = document.getElementById('menu')
loginbtn.addEventListener('click', () => {
    if(menu.className.split(/\s+/)[1] === 'login_list-active') {
        menu.classList.remove('login_list-active');
        loginbtn.classList.remove('login_img-white');
    } else {
        menu.classList.add('login_list-active');
        loginbtn.classList.add('login_img-white');
    }
});
