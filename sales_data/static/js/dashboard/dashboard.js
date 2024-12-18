console.log("dashboard loaded")
import { colors, create_total_meeting_data, create_type_meeting_data, create_type_meeting_structure,
        create_sales_eng_data_structure,create_sep_eng_sales_data, create_product_data,
        create_product_structure, meeting_tracker, Utils} from './dataset_functions.js'
const data                     = JSON.parse(document.getElementById("data").textContent);
const meeting_table_body       = document.getElementById('meeting_table_body');

const product_meeting_chart    = document.getElementById("product-chart").getContext('2d');
const total_meeting_chart      = document.getElementById("meeting-chart").getContext('2d');
const type_meeting_chart       = document.getElementById('type-meeting-chart').getContext('2d');
const sales_rep_meeting_chart  = document.getElementById('sales-rep-meeting-chart').getContext('2d');

//create labels
const labels                   = Utils.months({ count: 12 });

const create_meeting_data = () =>{
    const product_names       = create_product_structure(data);
    const total_meetings      = meeting_tracker(data['sales_eng_mgr']);
    const type_meetings       = create_type_meeting_structure(data);
    const sales_end_meetings  = create_sales_eng_data_structure(data['sales_eng_mgr']);


    const dataset = {
        type_meeting   : [],
        sales_rep_data : [],
        total_meetings : [],
        product_data   : [],
    }

    dataset['type_meeting']   = [...create_type_meeting_data(type_meetings)];
    dataset['sales_eng_data'] = [...create_sep_eng_sales_data(sales_end_meetings)];
    dataset['total_meetings'] = [...create_total_meeting_data(total_meetings)];
    dataset['product_data']   = JSON.parse(JSON.stringify(product_names));

    return dataset;
}

//Create sales eng meeting table row
const create_meeting_table_row = (sales_eng_data) =>{

    const tr = document.createElement('tr')

    meeting_table_body.append(tr);

    const name_cell = document.createElement("td");
    const iah_cell = document.createElement("td");
    const pa_cell = document.createElement("td");
    const fa_cell = document.createElement("td");
    name_cell.innerText = sales_eng_data[0];

    iah_cell.innerText = String(sales_eng_data[1]);
    pa_cell.innerText  = String(sales_eng_data[2]);
    fa_cell.innerText  = String(sales_eng_data[3]);

    tr.append(name_cell);
    tr.append(iah_cell);
    tr.append(fa_cell);
    tr.append(pa_cell);
}


const create_meeting_table_body_data = () =>{

    const table_data         = []
    const sales_meeting_data = data['sales_eng_mgr'];
    const manager_names      = Object.keys(sales_meeting_data);

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

    return table_data;
}

const sales_eng_meeting_data = create_meeting_table_body_data();
const chart_data             = create_meeting_data()

const table_display_default = () =>{

    if(!sales_eng_meeting_data){
        return
    }

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


    const line_chart = new Chart(sales_rep_meeting_chart, {
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
export const create_product_meeting_line = () =>{

    const product_labels = Object.keys(chart_data['product_data']);
    const product_values  = Object.values(chart_data['product_data']);
    const scatter_chart = new Chart(product_meeting_chart, {
        type: 'bar',
        data: {
            labels: product_labels,
            datasets: [
                {
                    label           : "Products",
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
export const create_type_meeting_line= () =>{

    const line_chart = new Chart(type_meeting_chart, {
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
create_product_meeting_line();
create_total_meeting_charts();
create_type_meeting_line();
table_display_default();
