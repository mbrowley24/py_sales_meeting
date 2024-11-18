console.log("load sales rep table");
import {value_format} from '../../validation.js'
const sales_reps = JSON.parse(document.getElementById("sales_rep_data").textContent)
const team_quota = document.getElementById("team_quota")
let team_quota_value = 0;

const table_body = document.getElementById("table_body");


const create_sales_rep_table = () =>{


    for(let i = 0; i < sales_reps.length; i++){
        const row       = document.createElement('tr');
        const role       = document.createElement("td");
        const first_name = document.createElement("td");
        const last_name  = document.createElement("td");
        const email      = document.createElement("td");
        const quota      = document.createElement("td");
        const updated_at = document.createElement("td");

        role.classList.add("capitalize")
        role.innerText                       = sales_reps[i].role?.toUpperCase()
        row.append(role);


        first_name.classList.add("capitalize")
        first_name.innerText                 = sales_reps[i].first_name
        row.append(first_name);


        last_name.classList.add("capitalize");
        last_name.innerText                  = sales_reps[i].last_name;
        row.append(last_name)

        email.classList.add("capitalize")
        email.innerText                      = sales_reps[i].email;
        row.append(email);

        let  quota_value                     = sales_reps[i].quota;

        if(isNaN(quota_value)){
                quota_value = 0
        }

        team_quota_value = team_quota_value + quota_value;

        quota.classList.add("capitalize")
        quota.innerText                      = `$${value_format(quota_value)}`
        row.append(quota)



        updated_at.classList.add("capitalize")
        updated_at.innerText                 = new Date(sales_reps[i].updated_at).toLocaleDateString()
        row.append(updated_at)


        table_body.append(row)

    }

    team_quota.innerText                    = `$${value_format(team_quota)}`;
}


create_sales_rep_table()