function CheckPassword(password) {
    var password = password;
    var special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
    var passwordMinLength = 8;
    var error_message = "";
    var contains_number = false;
    var contains_special = false;

    if (password.length < passwordMinLength) {
        error_message += "Password must be at least 8 characters in length!\n";
    }
    if (!isLetter(password[0])) {
        error_message += "Password must begin with a letter!\n";
    }
    for (i = 0; i < password.length; i++) {
        if (Number.isInteger(parseInt(password[i]))) {
            contains_number = true;
            break;
        }
    }
    for (i = 0; i < password.length; i++) {
        if ($.trim(password[i]) == '') {
            error_message += "Password cannot contain spaces!\n";
            break;
        }
    }

    if (!contains_number) {
        error_message += "Password must contain a number!\n";
    }
    for (i = 0; i < special_characters.length; i++) {
        if (password.includes(special_characters[i])) {
            contains_special = true;
            break;
        }
    }
    if (!contains_special) {
        error_message += "Password must contain a special character!\n";
    }
    return error_message;
}

function isLetter(str) {
    return str.length === 1 && str.match(/[a-z]/i);
}
