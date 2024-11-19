console.log("new Appointment loaded")
import {
    clean_text,
    clean_title,
    date_validation,
    text_validation,
    time_validation,
    title_validation} from "../validation.js"

$(document).ready(function () {
    $("#id_products").select2().on("select2:select", (e)=>{
        valid();
    })
});

const date                    = document.getElementById('id_date');
const date_error_message      = document.getElementById('date_error_message');
const notes                   = document.getElementById('id_notes');
const notes_error_message     = document.getElementById('notes_error_message');
const products                = document.getElementById('id_products');
const products_error_message  = document.getElementById('products_error_message');
const sales_rep               = document.getElementById("id_sales_representative");
const sales_rep_error_message = document.getElementById('sales_representative_error_message');
const save_button             = document.getElementById('save');
const time                    = document.getElementById('id_time');
const time_error_message      = document.getElementById('time_error_message')
const title                   = document.getElementById('id_title');
const title_error_message     = document.getElementById('title_error_message');
const type                    = document.getElementById('id_type');
const type_error_message      = document.getElementById('type_error_message')

const errors                  = {}



date.addEventListener("input", (e)=>{
    valid();
});

notes.addEventListener("input", (e)=>{
    const { value } = e.target;

    notes.value     = clean_title(value);

    valid();
});

products.addEventListener("change", (e)=>{
    console.log("in products")
    valid();
});

sales_rep.addEventListener('change', (e)=>{
    console.log("in saless rep")
    valid();
});

time.addEventListener('input', (e)=>{

    valid();
});

title.addEventListener("input", (e)=>{
    const { value } = e.target;

    title.value     = clean_title(value);

    valid();
});

type.addEventListener('change', (e)=>{
    console.log("type")
    valid()
})

const check_date = () =>{
    const date_text = date.value;

    if(date_text.trim() === "" || !date_text){

        errors['date'] = 'required';

    }else if(date_validation(date_text)){

        delete errors['date']

    }else{

        errors['date'] = 'invalid characters';
    }

    if(errors['date']){

        date_error_message.innerText = errors['date'];

    }else{

        date_error_message.innerText = "";

    }
}

const check_notes = () =>{
    const text_value = notes.value;

    if(text_value.trim() === "" || !text_value){

        errors['notes'] = 'required';

    }else if(text_validation(text_value)){

        delete errors['notes'];

    }else{

        errors['notes'] = 'invalid characters';

    }


    if(errors['notes']){

        notes_error_message.innerText = errors['notes']

    }else{

        notes_error_message.innerText = ""
    }
}


const check_products = () =>{

    for(let i = 0; i < products.childNodes.length; i++){

        const option = products.childNodes[i];

        if(option.selected && option.value !== ""){

            delete errors['products'];
             products_error_message.innerText = ""
            return
        }
    }


    errors['products'] = 'required';
    products_error_message.innerText = errors['products'];


}

const check_sales_rep = () =>{

    for(let i = 0; i < sales_rep.childNodes.length; i++){
        const option = sales_rep.childNodes[i];

        if(option.selected && option.value !== ""){

            delete errors['sales_rep'];
            sales_rep_error_message.innerText = "";
            return
        }
    }

    errors['sales_rep'] = 'required';
    sales_rep_error_message.innerText = errors['sales_rep'];
}

const check_time = () =>{
    const time_text = time.value;

    if(time_text.trim() === "" || !time_text){

        errors['time'] = 'required';

    }else if(time_validation(time_text)){

        delete errors['time']

    }else{

        errors['time'] = 'invalid characters';

    }

    console.log(errors)

    if(errors['time']){

        time_error_message.innerText = errors['time'];

    }else{

        time_error_message.innerText = "";
    }

}

const check_title = () =>{

    const title_text = title.value;

    if(title_text.trim() === "" || !title_text){

        errors['title'] = 'required';

    }else if(title_validation(title_text)){

        delete errors['title'];

    }else{

        errors['title'] = "invalid character(s)"
    }


    if(errors['title']){

        title_error_message.innerText = errors['title']

    }else{

        title_error_message.innerText = ""
    }


}
const check_type = () =>{



    for(let i = 0; i < type.childNodes.length; i++){

        const node = type.childNodes[i];

        if(node.selected && node.value !== ""){

            delete errors['type']
            type_error_message.innerText = "";
            return
        }

    }

    errors['type'] = 'required';
    type_error_message.innerText = errors['type'];
}



const valid = () =>{
    check_date();
    check_notes();
    check_products();
    check_sales_rep();
    check_time();
    check_title();
    check_type();
}

valid();