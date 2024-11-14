console.log("manager form loaded")
import {
    clean_email,
    clean_name,
    clean_username,
    email_validation,
    name_validation,
    password_check,
    username_validation,
} from "../../validation.js";
const confirm_password = document.getElementById("id_confirm_password");
const email = document.getElementById("id_email");
const email_error_message = document.getElementById("email_error_message");
const first_name = document.getElementById("id_first_name");
const first_name_error_message = document.getElementById("first_name_error_message");
const last_name = document.getElementById("id_last_name");
const last_name_error_message = document.getElementById("last_name_error_message");
const password = document.getElementById("id_password");
const password_message = document.getElementById("password_message");
const regions = document.getElementById("id_regions");
const region_error_message = document.getElementById("region_error_message")
const save = document.getElementById("save");
const timezones = document.getElementById('id_timezone');
const timezone_error_message = document.getElementById('timezone_error_message');
const username = document.getElementById("id_username");
const username_error_message = document.getElementById("username_error_message");

const errors = {};

const check_first_name = () =>{

    const first_name_value = first_name.value.trim()

    if(name_validation(first_name_value)){
        first_name_error_message.innerHTML = "Ok"
        first_name_error_message.classList.remove("errors")
        first_name_error_message.classList.add("success")

        delete errors['first_name']

    }else if (first_name_value.length === 0){

        first_name_error_message.innerHTML = "required"
        first_name_error_message.classList.remove("success")
        first_name_error_message.classList.add("errors")

        errors['first_name'] = 'required'
    }else{
        first_name_error_message.innerHTML = "required"
        first_name_error_message.classList.remove("success")
        first_name_error_message.classList.add("errors")


        errors['first_name'] = "invalid";
    }
}


const check_regions = () =>{

    let isValid = false;

    regions.childNodes.forEach(option => {

        if(option.value !== "" && option.selected){
            isValid = true;
        }
    })


    if(isValid){

        region_error_message.classList.remove('errors');
        region_error_message.classList.add("success");
        region_error_message.innerHTML = "ok";
        delete errors['region'];

    }else{

        region_error_message.classList.remove('success');
        region_error_message.classList.add('errors');
        region_error_message.innerHTML = "required";
        errors['region'] = 'required';

    }
}

const check_timezones = () =>{

    let isValid = false;

    timezones.childNodes.forEach(option => {

        if(option.value !== "" && option.selected){
            isValid = true;
        }
    })


    if(isValid){

        timezone_error_message.classList.remove('errors');
        timezone_error_message.classList.add("success");
        timezone_error_message.innerHTML = "ok";
        delete errors['timezone']

    }else{

        timezone_error_message.classList.remove('success');
        timezone_error_message.classList.add('errors');
        timezone_error_message.innerHTML = "required";
        errors['timezone'] = 'required';
    }
}

const check_password = () =>{

    const password_value = password.value.trim();
    const confirm_password_value = confirm_password.value

    if(password_value === ""){

        errors['password'] = "required"
        password_message.classList.remove('success');
        password_message.classList.add('errors');
        password_message.innerHTML = "required"
        return
    }

   if(password_check(password_value)){

       password_message.classList.remove('password-errors');
        password_message.classList.remove("errors");
        password_message.classList.add('success');
        password_message.innerHTML = "Ok"

        delete errors['password']

    }else{

       errors['password'] = "invalid"
       password_message.classList.remove('errors');
        password_message.classList.remove('success');
        password_message.classList.add('password-errors');
        password_message.innerHTML = "Min 8, 1 lowercase, 1 uppercase, special characters @$!%*?&"
        return

    }

    if(password_value === confirm_password_value){
        password_message.classList.remove('password-errors');
        password_message.classList.remove("errors");
        password_message.classList.add('success');
        password_message.innerHTML = "passwords match"

        delete errors['password']


    }else{

        errors['password'] = "invalid"
        password_message.classList.add('errors');
        password_message.classList.remove('success');
        password_message.classList.remove('password-errors');
        password_message.innerHTML = "passwords don't match"


    }

}


const check_last_name = () =>{

    const last_name_value = last_name.value.trim();

    if(name_validation(last_name_value)){
        last_name_error_message.innerHTML = "Ok"
        last_name_error_message.classList.remove("errors")
        last_name_error_message.classList.add("success")

        delete errors['last_name'];

    }else if (last_name_value.length === 0){

        last_name_error_message.innerHTML = "required"
        last_name_error_message.classList.remove("success")
        last_name_error_message.classList.add("errors")

        errors['last_name'] = 'required'

    }else{

        last_name_error_message.innerHTML = ""
        last_name_error_message.classList.remove("success")
        last_name_error_message.classList.add("errors")

        errors['last_name'] = 'invalid';
    }
}


const check_username = () =>{

    const username_value = username.value.trim();

    if(username_value === ""){
        username_error_message.innerHTML = "required"
        username_error_message.classList.add("errors")
        username_error_message.classList.remove("success")

        errors['username'] = 'required';
        return
    }

    if(!username_validation(username_value)){
        username_error_message.innerHTML = "invalid username"
        username_error_message.classList.add("errors")
        username_error_message.classList.remove("success")
        errors['username'] = "invalid"
        return
    }


    fetch(`/appManagement/managers/sales_engineers/check-username?username=${encodeURIComponent(username.value)}`,{
        method: "GET",
        headers:{
            "Content-Type": "application/json"
        }
    })
        .then(res=>{

            if(!res.ok){
                throw new Error("error")
            }
            return res.json();
        })
        .then(data =>{

            if(data.available){
                username_error_message.innerHTML = "available"
                username_error_message.classList.add("success")
                username_error_message.classList.remove("errors")
                delete errors['username']
            }else{
                username_error_message.innerHTML = "already taken"
                username_error_message.classList.add("errors")
                username_error_message.classList.remove("success")
                errors['username'] = data.message
            }
        })
        .catch(error =>{
            console.log(error)
        })

}


const check_email = () =>{
    const email_value = email.value.trim();

    if(email_value === ""){
        email_error_message.innerHTML = "required"
        email_error_message.classList.add("errors")
        email_error_message.classList.remove("success")
        return
    }

    if(!email_validation(email_value)){
        email_error_message.innerHTML = "invalid email"
        email_error_message.classList.add("errors")
        email_error_message.classList.remove("success")
        return
    }


    fetch(`/appManagement/managers/sales_engineers/check-email?email=${encodeURIComponent(email.value)}`,{
        method: "GET",
        headers:{
            "Content-Type": "application/json"
        }
    })
    .then(res=>{
        console.log(res)
        if(!res.ok){
            throw new Error("error")
        }
        return res.json();
    })
    .then(data =>{

        if(data.available){
            email_error_message.innerHTML = "available"
            email_error_message.classList.add("success")
            email_error_message.classList.remove("errors")
            delete errors['email']
        }else{
            email_error_message.innerHTML = "already taken"
            email_error_message.classList.add("errors")
            email_error_message.classList.remove("success")
        }


    })
    .catch(error =>{
        console.log(error)
    })
}


const show_errors = () =>{

    const error_list = document.createElement("ul");

    for (const key in errors){
        const list_item = document.createElement('li')
        list_item.innerHTML = `${key} : ${errors[key]}`

        error_list.append(list_item)
    }
}


confirm_password.addEventListener("input", (e)=>{

    check_password();
    valid()

});

email.addEventListener('input', (e)=>{
    const {value} = e.target;

    email.value = clean_email(value);

    check_email()
    valid()
})

first_name.addEventListener("input", (e)=>{
    const {value} = e.target;

    first_name.value = clean_name(value);
    check_first_name()
    valid()
});


last_name.addEventListener("input", (e)=>{
    const {value} = e.target;

    last_name.value = clean_name(value);

    check_last_name();
    valid()
});


password.addEventListener("input", (e)=>{
   const {value} = e.target;

    password.value = value;

    check_password();
    valid()

});

regions.addEventListener("change", (e) =>{

    check_regions();
    valid()
});

timezones.addEventListener("change", (e)=>{

    check_timezones();
    valid()

});

username.addEventListener("input", (e)=>{
    const {value} = e.target;

    username.value = clean_username(value)
    check_username()
    valid()

})

const valid = () =>{
    console.log(errors)
    save.disabled = Object.keys(errors).length > 0
}

// Run initial checks
check_email();
check_first_name();
check_last_name();
check_password();
check_regions();
check_timezones();
check_username();
valid();

