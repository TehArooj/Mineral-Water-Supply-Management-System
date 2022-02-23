let loginForm = document.getElementById("login");
let signUpForm = document.getElementById("signup");

const signUp = () => {
    loginForm.style.display = 'none'
    signUpForm.style.display = 'block'
}
const loginF = () => {
    loginForm.style.display = 'block'
    signUpForm.style.display = 'none'
}
const hashPassword = (pass) => {
    let hashedPass = ""
    for (let i = 0; i < pass.length; i++) {
        hashedPass += pass[i].charCodeAt(0);
    }
    return hashedPass;
}
const signUpFormSubmit = () => {
    let emailAddressUp = document.getElementById("emailAddressUp").value;
    let UserNameUp = document.getElementById('UserNameUp').value;
    let fullNameUp = document.getElementById('fullNameUp').value;
    let CnicUp = document.getElementById('CNICUp').value;
    let PhoneUp = document.getElementById('PhoneUp').value;
    let AddressUp = document.getElementById('AddressUp').value;
    let passwordUp = document.getElementById('passwordUp').value;
    let confirmPasswordUp = document.getElementById('confirmPasswordUp').value;
    let message = []
    if (emailAddressUp == "" ||UserNameUp=="" || fullNameUp == "" || AddressUp == "" || passwordUp == "" || confirmPasswordUp == "" ) {
        message.push("One or more field is empty")
    }
    if (passwordUp.length < 6) {
        message.push("Password Length is less than required(6 charaters)")
    }
    if (passwordUp != confirmPasswordUp) {
        message.push("Password Not Matching");
    }

    if (message.length == 0) {
        passwordUp = hashPassword(passwordUp);
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", '/signup', true);
        let userDetails = {
            email: emailAddressUp,
            userName: UserNameUp,
            name: fullNameUp,
            cnic:CnicUp,
            phone:PhoneUp,
            address:AddressUp,
            password: passwordUp,
        }
        xhttp.send(JSON.stringify(userDetails))
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                message.push(xhttp.responseText);
                console.log(xhttp.responseText)
                if (message[0] != "Account Created Sucessfully") {
                    printErrors(message);
                } else {
                    window.location = '/signup'
                }
            }
        }
    }
    printErrors(message);
}

const printErrors = (m) => {
    let errors = document.getElementById('errors')
    console.log(m[0])
    errors.innerHTML = ''
    errors.innerHTML = '<ol>'
    for (let i = 0; i < m.length; i++) {
        errors.innerHTML += '<li>' + m[i] + '</li>'
    }
    errors.innerHTML += '<ol>'
}

const loginFunc = () => {
    let email = document.getElementById('emailAddress').value;
    let password = document.getElementById('password').value;
    let message = []

    if (email == "" || password == "") {
        alert("Either Email or password field is empty")
        return;
    }
    password = hashPassword(password);
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/signin', true);
    let userDetails = {
        email: email,
        password: password,
    }
    xhttp.send(JSON.stringify(userDetails))
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var response= xhttp.responseText;
            var data= JSON.parse(response)
            console.log("data: ",data);
            if(data=='3'){
                console.log("cust")
                window.location='/custDashboard';
            }
            if(data=='1'){
                console.log("admin")
                window.location='/Dashboard';
            }
            else{
                console.log('wrong Email or password!!!');
            }
        }
        else{
            console.log("Waiting for response")
        }
    }
}