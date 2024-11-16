                      console.log("manager form loaded")
import {
    clean_email,
    clean_name,
    email_validation,
    name_validation,
    value_format,
    value_valid,
} from "../../validation.js";

const email = document.getElementById("id_email");
const email_error_message = document.getElementById("email_error_message");
const first_name = document.getElementById("id_first_name");
const first_name_error_message = document.getElementById("first_name_error_message");
const last_name = document.getElementById("id_last_name");
const last_name_error_message = document.getElementById("last_name_error_message");
const quota = document.getElementById("id_quota");
const quota_message = document.getElementById("quota_message");
const role = document.getElementById("id_role");
const role_message = document.getElementById("role_message");
const sales_engineers = document.getElementById("id_sales_engineer");
const sales_engineer_message = document.getElementById("sales_engineer_message");
const save = document.getElementById("save");


const errors = {};

const init_quota = () =>{

    quota.value = "0.00"
}

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

const check_quota = () =>{

    const test = quota.value
    console.log(value_valid(test))
    if(!value_valid(test)){

        quota_message.innerText =  "required"

        errors['quota'] = "invalid value";


    }else{

        quota_message.innerText = "";
        delete errors['quota'];

    }

}

const check_role = () =>{

    let valid = false;
    for(let i = 0; i < role.childNodes.length; i++){

        const option = role.childNodes[i];


        if(option.selected && option.value !== ""){
            console.log("here here man")
            valid = true;
        }

    }

    if(!valid){

        role_message.innerText = "required"

        errors['role'] = 'required';

    }else{

        role_message.innerText = ""

        delete errors['role']

    }
}


const check_sales_engineer = () =>{

    let valid = false;

    for(let i = 0; i < sales_engineers.childNodes.length; i++){

        const option = sales_engineers.childNodes[i];

        if(option.selected && option.value !== ""){
            console.log("in sales engineer")
            valid = true;
        }
    }





    if(!valid){

        sales_engineer_message.innerText = "required";

        errors['sales_engineer'] = 'required';

    }else{

        sales_engineer_message.innerText = "";
        delete errors['sales_engineer'];

    }

}


const check_sales_engineer_init = () =>{

    if(!errors['sales_engineer']){
        console.log("here")
        sales_engineers.disabled = true
    }

}


const check_email = () =>{
    const email_value = email.value.trim();

    console.log(email_value)
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


    fetch(`/appManagement/managers/sales_reps/check-username?email=${encodeURIComponent(email.value)}`,{
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


email.addEventListener('input', (e)=>{
    const {value} = e.target;

    email.value = value;

    valid()
})

first_name.addEventListener("input", (e)=>{
    const {value} = e.target;

    first_name.value = clean_name(value);
    valid()
});


last_name.addEventListener("input", (e)=>{
    const {value} = e.target;

    last_name.value = clean_name(value);
    valid()

});



email.addEventListener("input", (e)=>{
    const {value} = e.target;

    email.value = value;
    valid();

});

quota.addEventListener("input", (e)=>{
   const {value} = e.target;
    console.log(value)

    quota.value = value_format(value);
    valid()

});

role.addEventListener("change", (e)=>{

    valid();
});

sales_engineers.addEventListener("change", (e)=>{

    valid();
})



const valid = () =>{
    check_email();
    check_first_name();
    check_last_name();
    check_role();
    check_sales_engineer();
    check_quota()
    save.disabled = Object.keys(errors).length > 0
}


init_quota()
valid();
check_sales_engineer_init()
console.log(errors)
