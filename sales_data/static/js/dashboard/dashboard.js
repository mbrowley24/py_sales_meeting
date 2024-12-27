console.log("dashboard loaded")
import { colors, create_total_meeting_data, create_type_meeting_data, create_sales_eng_data_structure,
        create_sep_eng_sales_data, create_product_structure, meeting_tracker, sales_eng_list,
    Utils} from './dataset_functions.js';

const data                     = JSON.parse(document.getElementById("data").textContent);
const meeting_table_body       = document.getElementById('meeting_table_body');
const eng_name                 = document.getElementById("eng_name");
const iah_col                  = document.getElementById("iah_count");
const pa_col                   = document.getElementById("pa_count");
const fa_col                   = document.getElementById("fa_count");
const product_eng              = document.getElementById("product_eng");
const type_eng                 = document.getElementById("type_eng")

const product_meeting_chart    = document.getElementById("product-chart").getContext('2d');
const total_meeting_chart      = document.getElementById("meeting-chart").getContext('2d');
const type_meeting_chart       = document.getElementById('type-meeting-chart').getContext('2d');
const sales_rep_meeting_chart  = document.getElementById('sales-rep-meeting-chart').getContext('2d');

//create labels
const labels                   = Utils.months({ count: 12 });
const sales_eng_name_list      = sales_eng_list(data);

const create_meeting_data = () =>{
    const product_names       = create_product_structure(data, '');
    const total_meetings      = meeting_tracker(data['sales_eng_mgr']);
    const sales_end_meetings  = create_sales_eng_data_structure(data['sales_eng_mgr']);


    const dataset = {
        type_meeting   : [],
        sales_rep_data : [],
        total_meetings : [],
        product_data   : [],
    }

    dataset['type_meeting']   = [...create_type_meeting_data(data, "")];
    dataset['sales_eng_data'] = [...create_sep_eng_sales_data(sales_end_meetings)];
    dataset['total_meetings'] = [...create_total_meeting_data(total_meetings)];
    dataset['product_data']   = JSON.parse(JSON.stringify(product_names));

    return dataset;
}



//Create sales eng meeting table row
const create_meeting_table_row = (sales_eng_data) =>{

    const tr = document.createElement('tr')

    meeting_table_body.append(tr);

    const name_cell     = document.createElement("td");
    const iah_cell      = document.createElement("td");
    const pa_cell       = document.createElement("td");
    const fa_cell       = document.createElement("td");
    name_cell.innerText = sales_eng_data[0];

    iah_cell.innerText  = String(sales_eng_data[1]);
    pa_cell.innerText   = String(sales_eng_data[2]);
    fa_cell.innerText   = String(sales_eng_data[3]);

    tr.append(name_cell);
    tr.append(iah_cell);
    tr.append(fa_cell);
    tr.append(pa_cell);
}


const create_meeting_table_body_data = () =>{

    const table_data         = []
    const sales_meeting_data = data['sales_eng_mgr'];
    const manager_names      = Object.keys(sales_meeting_data);

    eng_name.dataset.order = "desc";

    for(let i = 0; i < manager_names.length; i++){

        const sales_eng_data  = JSON.parse(JSON.stringify(sales_meeting_data[manager_names[i]]));

        const sales_eng_names = Object.keys(sales_eng_data);

        for(let j = 0; j < sales_eng_names.length; j++){

            const sales_eng_stats  = [sales_eng_names[j], 0, 0, 0];

            const sales_reps_data  = JSON.parse(JSON.stringify(sales_eng_data[sales_eng_names[j]]));
            const sales_reps_names = Object.keys(sales_reps_data);


            for(let k = 0; k < sales_eng_names.length; k++){

                const meeting_list = [...sales_reps_data[sales_reps_names[k]]];

                for(let l = 0; l < meeting_list.length; l++){

                    const type = meeting_list[l].type;

                    if(type === "iah"){

                        sales_eng_stats[1]++

                    }else if(type === "pa"){

                        sales_eng_stats[2]++

                    }else if(type === "fa"){

                        sales_eng_stats[3]++
                    }
                }
            }

            table_data.push(sales_eng_stats);
        }
    }

    return table_data.sort((a, b) => a[0].localeCompare(b[0], { sensitivity: 'base' }));
}

const populate_sales_eng_names = () =>{

    function capitalize(name_string){
        const name_list    = name_string.split(" ");
        const first_name   = `${name_list[0].charAt(0).toUpperCase()}${name_list[0].substring(1, name_list[0].length)}`
        const last_name    = `${name_list[1].charAt(0).toUpperCase()}${name_list[1].substring(1, name_list[1].length)}`

        return `${first_name} ${last_name}`
    }


    for(let i = 0; i < sales_eng_name_list .length; i++){

        const option       = document.createElement('option');
        const name         = sales_eng_name_list[i]
        option.value       = name;
        option.innerText   = capitalize(name);

        product_eng.append(option);
    }

    for(let i = 0; i < sales_eng_name_list.length; i++){

        const option       = document.createElement('option');
        const name         = sales_eng_name_list[i]
        option.value       = name;
        option.innerText   = capitalize(name);

        type_eng.append(option);
    }



}


let   sales_eng_meeting_data  = create_meeting_table_body_data()
const chart_data              = create_meeting_data()

const table_display = (sales_eng_meeting_data) =>{

    if(!sales_eng_meeting_data){
        return
    }

    meeting_table_body.innerHTML = "";



    for(let i = 0; i < sales_eng_meeting_data.length; i++){

        create_meeting_table_row(sales_eng_meeting_data[i]);

    }
}



//create_total_meeting_charts creates a total meeting chart
const create_total_meeting_charts = () =>{

    const bar_chart = new Chart(total_meeting_chart, {
        type : 'bar',
        data : {
            labels   : labels,
            datasets : chart_data['total_meetings']
        },
        options : {
            scales : {
                y: {
                    min     : 0,
                    stacked : true
                }
            },
            responsive : true,
            maintainAspectRatio : false,
            plugins:{
                legend:{
                    display : false,
                    labels:{
                        font:{
                            size: 12
                        }
                    }
                }
            }
        }
    })
}

//create_sales_reps_meeting_number create chart for tracking for sales rep meeting
const create_sales_reps_meeting_data = () =>{


    return new Chart(sales_rep_meeting_chart, {
        type    : 'line',
        data    : {
            labels   : labels,
            datasets : chart_data['sales_eng_data']
        },
        options : {
            scales :{
                y :{
                    min     : 0,
                    stacked : 0
                }
            },
          responsive: true,
          maintainAspectRatio: false,
          plugins:{
                legend:{
                    display : true,
                    labels:{
                        font:{
                            size: 8
                        }
                    }
                }
            }
        }

    })

};


// //create type meetings line in graph
export const create_product_meeting_line = (data) =>{

    const product_labels = Object.keys(chart_data['product_data']);
    const product_values  = Object.values(chart_data['product_data']);

    return new Chart(product_meeting_chart, {
        type: 'bar',
        data: {
            labels: product_labels,
            datasets: [
                {
                    label           : "",
                    data            : product_values,  // Correcting datasets structure
                    backgroundColor : [...colors],
                    borderColor     : [...colors],
                    borderWidth     : 1
                }
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display : false,
                    labels: {
                        font: {
                            size: 15
                        },
                    }
                }
            }
        }
    });
}

//create type meetings line in graph
const create_type_meeting_line= () =>{

    return new Chart(type_meeting_chart, {
        type    : 'line',
        data    : {
            labels   : labels,
            datasets : chart_data['type_meeting'],
        },
        options : {
            scales    : {
                y : {
                    min     : 0,
                    stacked : true
                }
            },
            responsive          : true,
            maintainAspectRatio : false, // Allow custom width/height ratios
            plugins:{
                legend:{
                    labels:{
                        font:{
                            size: 14
                        }
                    }
                }
            }
        }
    })
}


create_meeting_data();
create_sales_reps_meeting_data();
const product_chart  = create_product_meeting_line();
const type_chart     = create_type_meeting_line();
create_total_meeting_charts();
table_display(sales_eng_meeting_data);
populate_sales_eng_names()


eng_name.addEventListener("click", (e)=>{

    const order = eng_name.dataset.order === "asc" ? "desc" : 'asc'

    iah_col.dataset.order = "";
    pa_col.dataset.order  = "";
    fa_col.dataset.order  = "";

    eng_name.dataset.order = order;

   if(order === "asc"){

        sales_eng_meeting_data.sort((a, b) =>{

            if(a[0].toLowerCase().localeCompare(b[0].toLowerCase()) === 0){

                return a[1] - b[1]
            }

            return a[0].toLowerCase().localeCompare(b[0].toLowerCase());
       })

    }else if(order === "desc"){

        sales_eng_meeting_data.sort((a, b) =>{

            if(a[0].toLowerCase().localeCompare(b[0].toLowerCase()) === 0){

                return b[1] - a[1]
            }

            return b[0].toLowerCase().localeCompare(a[0].toLowerCase());

        } )
    }

    table_display(sales_eng_meeting_data)
})


iah_col.addEventListener('click', (e)=>{

    const order = iah_col.dataset.order === "asc" ? "desc" : 'asc'

    eng_name.dataset.order = "";
    pa_col.dataset.order   = "";
    fa_col.dataset.order   = "";

    iah_col.dataset.order  = order;

    if(order === "asc"){

        sales_eng_meeting_data.sort((a, b) => {

            if(a[1] === b[1]){

                return a[0].toLowerCase().localeCompare(b[0].toLowerCase())
            }

            return a[1] - b[1]
        })

    }else if(order === "desc"){

        sales_eng_meeting_data.sort((a, b) =>{

            if(a[1] === b[1]){

                return b[0].toLowerCase().localeCompare(a[0].toLowerCase())
            }

            return b[1] - a[1]
        })
    }

    table_display(sales_eng_meeting_data)

})

pa_col.addEventListener('click', (e)=>{

    const order = pa_col.dataset.order === "asc" ? "desc" : 'asc'

    eng_name.dataset.order = "";
    iah_col.dataset.order  = "";
    fa_col.dataset.order   = "";

    pa_col.dataset.order = order;

    if(order === "asc"){

        sales_eng_meeting_data.sort((a, b) => {

            if(a[2] === b[2]){

                return a[0].toLowerCase().localeCompare(b[0].toLowerCase())
            }

            return a[2] - b[2]
        })

    }else if(order === "desc"){

        sales_eng_meeting_data.sort((a, b) =>{

            if(a[2] === b[2]){

                return b[0].toLowerCase().localeCompare(a[0].toLowerCase())
            }

            return b[2] - a[2]
        })
    }

    table_display(sales_eng_meeting_data)
})


fa_col.addEventListener('click', (e)=>{

    const order = fa_col.dataset.order === "asc" ? "desc" : 'asc'

    eng_name.dataset.order = "";
    iah_col.dataset.order  = "";
    pa_col.dataset.order   = "";

    fa_col.dataset.order   = order;

    if(order === "asc"){

        sales_eng_meeting_data.sort((a, b) => {

            if(a[3] === b[3]){

                return a[0].toLowerCase().localeCompare(b[0].toLowerCase())
            }

            return a[3] - b[3]
        })

    }else if(order === "desc"){

        sales_eng_meeting_data.sort((a, b) =>{

            if(a[3] === b[3]){

                return b[0].toLowerCase().localeCompare(a[0].toLowerCase())
            }

            return b[3] - a[3]
        })
    }

    table_display(sales_eng_meeting_data)

})


product_eng.addEventListener("change", (e) =>{

    chart_data['product_data'] = create_product_structure(data, e.target.value);

    console.log(chart_data['product_data'])
    product_chart.data.datasets[0].data = Object.values(chart_data['product_data']);
    product_chart.update()
})

type_eng.addEventListener("change", (e) =>{
    console.log('here here')
    chart_data['type_meeting'] = [...create_type_meeting_data(data, e.target.value)];

    console.log(chart_data['type_meeting'])
    type_chart.data.datasets = chart_data['type_meeting']
    type_chart.update()

})