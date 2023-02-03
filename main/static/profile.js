function default_input(element) {
    element.readonly = 'readonly';
}

username_input = document.getElementById('username');
username_input.setAttribute('readonly', 'readonly');
email_input = document.getElementById('email')
email_input.setAttribute('readonly', 'readonly');
intro_input = document.getElementById('intro')
intro_input.setAttribute('readonly', 'readonly');

btn_for_username = document.getElementById('edit_username');
btn_for_email = document.getElementById('edit_email');
btn_for_intro = document.getElementById('edit_intro');
btn_for_username.addEventListener('click', function () {
    if (username_input.hasAttribute('readonly')) {
        console.log(this)
        username_input.removeAttribute('readonly');
        username_input.classList.remove('form-control-plaintext');
        this.innerText = '确认';
    } else {
        username_input.setAttribute('readonly', 'readonly');
        username_input.classList.add('form-control-plaintext');
        this.innerText = '修改';
    }
})
btn_for_email.addEventListener('click', function () {
    if (email_input.hasAttribute('readonly')) {
        console.log(this)
        email_input.removeAttribute('readonly');
        email_input.classList.remove('form-control-plaintext');
        this.innerText = '确认';
    } else {
        email_input.setAttribute('readonly', 'readonly');
        email_input.classList.add('form-control-plaintext');
        this.innerText = '修改';
    }
})
btn_for_intro.addEventListener('click', function () {
    if (intro_input.hasAttribute('readonly')) {
        console.log(this)
        intro_input.removeAttribute('readonly');
        intro_input.classList.remove('form-control-plaintext');
        this.innerText = '确认';
    } else {
        intro_input.setAttribute('readonly', 'readonly');
        intro_input.classList.add('form-control-plaintext');
        this.innerText = '修改';
    }
})
