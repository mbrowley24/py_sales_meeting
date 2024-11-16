console.log("sales rep  admin table")

import {value_format} from "../../validation.js"


const sales_representatives_data = JSON.parse(document.getElementById("sales_representatives_data").textContent);

const table_body = document.getElementById("table-body");
const base_url = "/appManagement/managers/sales_engineers/"

const create_sales_engineer_row = (sales_rep) =>{
    const table_row = document.createElement('tr');

    console.log(sales_rep)

    const role = document.createElement('td');
    role.classList.add("capitalize");
    role.innerText = sales_rep.role?.toUpperCase();
    table_row.append(role);

    //first_name cell
    const first_name = document.createElement('td');
    first_name.classList.add("capitalize")
    first_name.innerText = sales_rep.first_name;

    table_row.append(first_name);

    //last_name cell
    const last_name = document.createElement('td');
    last_name.classList.add("capitalize");
    last_name.innerText = sales_rep.last_name;
    table_row.append(last_name);

    const email = document.createElement('td')
    email.contentEditable="true"
    email.innerText = sales_rep.email;
    table_row.append(email);


    const quota = document.createElement("td");
    quota.innerText = `$${value_format(sales_rep.quota)}`;
    quota.classList.add("capitalize")
    table_row.append(quota);



    const edit = document.createElement("td");
    const edit_link = document.createElement('a');

    edit_link.href = `/appManagement/managers/sales_engineers/edit/${sales_rep.id}`
    edit_link.innerText = "edit"
    edit.append(edit_link)

    table_row.append(edit);

    return table_row
}



const sales_engineer_table = () =>{

    for(let i = 0; i < sales_representatives_data.length; i++){
        console.log(sales_representatives_data[i])

        table_body.append(create_sales_engineer_row(sales_representatives_data[i]));
    }



}

sales_engineer_table()