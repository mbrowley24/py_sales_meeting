console.log("appointment table")

const appointment_data   = JSON.parse(document.getElementById("appointments_data").textContent);
const table_body         = document.getElementById("table-body");
const product_search     = document.getElementById('search');
const clear              = document.getElementById('clear');
let product_search_items = [];
const products           = [];

$(document).ready(function () {
    const select = $("#search");

    select.select2();
    // select.select2().on("select2:select", (e)=>{
    //     console.log("change")
    //     create_product_list();
    //     create_table_rows();
    // });

    select.on('change', ()=>{
        create_product_list();
        create_table_rows();
    })

    product_selection();
    create_product_list()

});

const create_table_rows = () =>{

    table_body.replaceChildren();
    console.log("in here")
    if(product_search_items.length === 0){

        console.log('no items')

        for(let i = 0; i < appointment_data.length; i++){
            create_table_row(appointment_data[i])
        }

        return
    }


    if(product_search_items.length > 0){
        console.log("items in here")
         for(let i = 0; i < appointment_data.length; i++) {

             let interesting = false;

             const products = [...appointment_data[i].products];

             for (let i = 0; i < products.length; i++) {

                 if (product_search_items.includes(products[i])) {
                     interesting = true;
                     break;
                 }
             }

             if (!interesting) continue;

             create_table_row(appointment_data[i])
         }
    }
}

const create_table_row = (appointment) =>{


        const row                   = document.createElement("tr");
        const time                  = document.createElement('td');
        const date                  = document.createElement('td');
        const type                  = document.createElement('td');
        const title                 = document.createElement('td');
        const sales_reps            = document.createElement('td');
        const edit                  = document.createElement('td');
        const edit_appointment_link = document.createElement('a')

        time.innerText              = appointment.time
        row.append(time);

        date.innerText              = appointment.date;
        row.append(date);

        type.innerText              = appointment.type?.toUpperCase()
        row.append(type);

        title.innerText             = appointment.title;
        title.classList.add("capitalize");
        row.append(title);

        sales_reps.innerText        = appointment.sales_rep;
        sales_reps.classList.add("capitalize");
        row.append(sales_reps);


        edit_appointment_link.innerText = "edit"

        edit.append(edit_appointment_link)
        row.append(edit);

        collect_products(appointment.products)
        table_body.append(row);


}


const collect_products = (product_values) =>{

    for(let i = 0; i < product_values.length; i++){

        if(!products.includes(product_values[i])){

            products.push(product_values[i])

        }

    }

}

const product_selection = () =>{



    for(let i = 0; i < products.length; i++ ){

        const option     = document.createElement('option');

        option.innerText = products[i].toUpperCase();
        option.value     = products[i];

        product_search.appendChild(option)
    }


}

const create_product_list = () =>{

    product_search_items = [];

    for(let i = 0; i < product_search.childNodes.length; i++){

        if(product_search.childNodes[i].selected && product_search.childNodes[i].value !== ""){

            product_search_items.push(product_search[i].value);

        }
    }


}

create_table_rows();


