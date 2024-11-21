console.log("dashboard loaded")
import {create_total_meeting_data, create_type_meeting_data, create_type_meeting_structure,
        create_sales_reps_data_structure,create_sep_rep_sales_data, create_product_data,
        create_product_structure, Utils} from './dataset_functions.js'
const appointment_data        = JSON.parse(document.getElementById("appointment_data").textContent);
const product_name_list       = JSON.parse(document.getElementById("products").textContent);
const sales_reps              = JSON.parse(document.getElementById("sales_reps").textContent);
const appointment_type_names   = JSON.parse(document.getElementById('appointment_type_names').textContent);
const product_meeting_chart   = document.getElementById("product-chart").getContext('2d');
const total_meeting_chart     = document.getElementById("meeting-chart").getContext('2d');
const type_meeting_chart      = document.getElementById('type-meeting-chart').getContext('2d');
const sales_rep_meeting_chart = document.getElementById('sales-rep-meeting-chart').getContext('2d');
console.log(appointment_data)

//create labels
const labels                  = Utils.months({ count: 12 });


const create_meeting_data = () =>{
    const product_names   = create_product_structure(product_name_list)
    const total_meetings  = Array(12).fill(0);
    const type_meetings   = create_type_meeting_structure(appointment_type_names);
    const sales_rep_data  = create_sales_reps_data_structure(sales_reps);
    const dataset = {
        type_meeting   : [],
        sales_rep_data : [],
        total_meetings : [],
        product_data  : [],

    }

    for(let i = 0; i < appointment_data.length; i++){

        const month_index            = (new Date(appointment_data[i].date).getMonth() - 1)

        //appointment type name
        const type_name              = appointment_data[i].type;

        //sales rep name
        const sales_rep_name         = appointment_data[i].sales_rep;

        const product_name_list      = [...appointment_data[i].products];

        total_meetings[month_index] += 1

        //get meeting type data
        if(type_meetings[type_name]){

            type_meetings[type_name][month_index]              += 1

        }else{

            type_meetings[type_name]               = Array(12).fill(0)
            type_meetings[type_name][month_index] += 1

        }


        // //get sales rep type data
        if(sales_rep_data[sales_rep_name]){

           sales_rep_data[sales_rep_name][month_index] += 1

        }else{

            sales_rep_data[sales_rep_name]               = [...Array(12).fill(0)]
            sales_rep_data[sales_rep_name][month_index] += 1
        }

        for(let i =0; i < product_name_list.length; i++){

            const name = product_name_list[i]

            if(product_names[name]){

                product_names[name][month_index] += 1

            }else{

                product_names[name] = [...Array(12).fill(0)]
                product_names[name][month_index] += 1

            }
        }






    }

    dataset['type_meeting']   = [...create_type_meeting_data(type_meetings)];
    dataset['sales_rep_data'] = [...create_sep_rep_sales_data(sales_rep_data)];
    dataset['total_meetings'] = [...create_total_meeting_data(total_meetings)];
    dataset['product_data']   = [...create_product_data(product_names)];

    return dataset;
}

 const chart_data = create_meeting_data()

//create_total_meeting_charts creates a total meeting chart
const create_total_meeting_charts = () =>{

     console.log(chart_data['total_meetings'])
    const line_chart = new Chart(total_meeting_chart, {
        type : 'line',
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
            datasets : chart_data['sales_rep_data']
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


//create type meetings line in graph
export const create_product_meeting_line = () =>{

    const line_chart = new Chart(product_meeting_chart, {
        type    : 'line',
        data    : {
            labels   : labels,
            datasets : chart_data['product_data'],
        },
        options : {
            scales    : {
                y : {
                    min     :   0,
                    stacked : true
                }
            },
            responsive          : true,
            maintainAspectRatio : false,
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
