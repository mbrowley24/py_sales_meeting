console.log("sales engineer table")

const sales_engineer_data = JSON.parse(document.getElementById("sales_engineers_data").textContent);

const table_body = document.getElementById("table-body");
const base_url = "/appManagement/managers/sales_engineers/"

const create_sales_engineer_row = (sales_engineer) =>{
    const table_row = document.createElement('tr');



    //first_name cell
    const first_name = document.createElement('td');
    first_name.classList.add("capitalize")
    first_name.innerText = sales_engineer.first_name;

    table_row.append(first_name);

    //last_name cell
    const last_name = document.createElement('td');
    last_name.innerText = sales_engineer.last_name;
    last_name.classList.add("capitalize")
    table_row.append(last_name);

    const email = document.createElement('td')
    email.contentEditable="true"
    email.innerText = sales_engineer.email;
    table_row.append(email);

    const sales_reps = document.createElement("td");
    const sales_rep_link = document.createElement('a');
    sales_rep_link.innerText = sales_engineer.sales_reps
    sales_rep_link.href = `${base_url}edit/${sales_engineer.id}/sales_reps`
    sales_reps.append(sales_rep_link)
    table_row.append(sales_reps);

    const manager = document.createElement("td")
    table_row.append(manager);

    if(sales_engineer.manager){

        manager.innerText = sales_engineer.manager

    }else{

        manager.innerText = "Not Assigned"

    }



    const region = document.createElement("td");
    region.innerText = sales_engineer.region
    region.classList.add("capitalize")
    table_row.append(region);

    const last_login =  document.createElement("td");

    if(sales_engineer.last_login){

        last_login.innerText = new Date(sales_engineer.last_login).toLocaleDateString()

    }else{

        last_login.innerText = "Never"
    }

    table_row.append(last_login)

    const edit = document.createElement("td");
    const edit_link = document.createElement('a');

    edit_link.href = `/appManagement/managers/sales_engineers/edit/${sales_engineer.id}`
    edit_link.innerText = "edit"
    edit.append(edit_link)

    table_row.append(edit);

    return table_row
}



const sales_engineer_table = () =>{

    for(let i = 0; i < sales_engineer_data.length; i++){
        console.log(sales_engineer_data[i])

        table_body.append(create_sales_engineer_row(sales_engineer_data[i]));
    }

    console.log(table_body)

}

sales_engineer_table()