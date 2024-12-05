console.log("loaded customer")

import {
    clean_name,
    clean_text,
    name_validation,
    text_validation,
} from '/static/js/validation.js'

//field with event listener
const name           = document.getElementById("id_name");
const notes          = document.getElementById("id_notes");
const sales_eng      = document.getElementById('id_sales_engineer');
const sales_rep      = document.getElementById("id_sales_rep");
const sales_engineer = document.getElementById('id_sales_engineer');
const save           = document.getElementById('save');
const vertical       = document.getElementById("id_vertical");
const selected_eng   = document.getElementById('sales_eng');

//error message elements
const name_error_messages       = document.getElementById("name_error_message");
const notes_error_messages      = document.getElementById("notes_error_message");
const sales_reps_error_messages = document.getElementById("sales_rep_error_message");
const sales_eng_error_messages  = document.getElementById('sales_eng_error_message');
const vertical_error_messages   = document.getElementById("vertical_error_message")

//collect error messages
const errors = {}

name.addEventListener('input', (e)=>{
    const { value } = e.target;

    name.value = clean_name(value);

    valid();
});

notes.addEventListener("input", (e)=>{
    const { value } = e.target;

    notes.value = clean_text(value)

    valid();

});

sales_engineer.addEventListener('change', (e)=>{

    valid();
})

sales_rep.addEventListener('change', (e)=>{

    valid()
});

vertical.addEventListener('input', (e)=>{

    valid();

});

const check_errors_messages = () =>{
    console.log("here here")
    let is_valid                             = true;
    const name_error_message_check           = name_error_messages.innerText;
    const notes_error_message_check          = notes_error_messages.innerText;
    const sales_rep_error_message_check      = sales_reps_error_messages.innerText;
    const sales_engineer_error_message_check = sales_eng_error_messages.innerText;
    const vertical_error_message_check       = vertical_error_messages.innerText;

    if(name_error_message_check.length > 0){

        is_valid = false;

    }

    if(notes_error_message_check.length > 0){

        is_valid = false;
    }

    if(sales_rep_error_message_check.length > 0){

        is_valid = false;
    }

    if(sales_engineer_error_message_check.length > 0){

        is_valid = false;
    }

    if(vertical_error_message_check.length > 0){

        is_valid = false;
    }

    save.disabled = !is_valid;
}

const check_name_validation = () =>{

    //trim name and name value
    const name_value = name.value.trim()

    //check characters in name
    if(!name_validation(name_value)){

        errors['name'] = "invalid character";
    }

    //check if name length is 0 or grater 100
    //if less than 0 or greater than 100 then generator error
    if(name_value.length === 0){

        errors['name'] = "required";

    }

    //check name length and character are valid and remove errors if valid
    if(name_value.length > 2 && name_value.length <= 100){

        if(name_validation(name_value)){

            delete errors['name'];

        }
    }

    if(errors['name'] && name_error_messages){


        name_error_messages.innerText = errors['name'];

    }else{

        delete errors['name'];

        if(name_error_messages){
            name_error_messages.innerText = "";
        }
    }

}

const check_notes_validation = () => {

    const notes_text = notes.value.trim()

    if (!text_validation(notes_text)) {

        errors['notes'] = "invalid character"
    }


    if (errors['notes']) {

        notes_error_messages.innerText = errors['notes'];

    } else {

        notes_error_messages.innerText = "";

    }

}


const sales_engineer_check = () =>{
    let is_valid = false;

    for(let i = 0; i < sales_engineer.childNodes.length; i++){

        const option = sales_engineer.childNodes[i];

        if(option.selected && option.value !== ""){

            is_valid = true;

        }
    }

    if(!is_valid && sales_eng_error_messages){

        errors['sales_engineer']           = 'required';
        sales_eng_error_messages.innerText = errors['sales_engineer'];

    }else{

        delete errors['sales_engineer'];

        if(sales_eng_error_messages){
            sales_eng_error_messages.innerText = ""
        }
    }
}

const sales_rep_check = () =>{

    let is_valid = false;

    for(let i = 0; i < sales_rep.childNodes.length; i++){

        const option = sales_rep.childNodes[i];

        if(option.selected && option.value !== ""){
            is_valid = true;
            break;
        }
    }

    if(!is_valid){

        errors['sales_rep'] = 'required';
        sales_reps_error_messages.innerText = errors['sales_rep'];

    }else{

        delete errors['sales_rep'];
        sales_reps_error_messages.innerText = "";

    }
}

const vertical_check = () => {

    let is_valid = false;

    for(let i = 0; i < vertical.childNodes.length; i++){

        const option = vertical.childNodes[i];

        if(option.selected && option.value !== ''){

            is_valid = true;
            break
        }
    }

    if(is_valid){

        delete errors['vertical'];
        vertical_error_messages.innerText = "";

    }else{

        errors['vertical'] = 'required';
        vertical_error_messages.innerText = errors['vertical'];
    }
}

const valid = () => {


    check_name_validation();
    check_notes_validation();
    sales_engineer_check();
    sales_rep_check();
    vertical_check();
    save_button();

}


const save_button = () =>{
    const error_keys = Object.keys(errors);

    save.disabled = error_keys.length > 0;
}


const check_sales_engineer = () =>{
    console.log(sales_eng.value);

    if(sales_eng.value){

        sales_eng.disabled = true;
    }
}

check_sales_engineer();
valid();
// check_errors_messages();