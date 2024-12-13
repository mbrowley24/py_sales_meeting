console.log("dashboard loaded")
import {create_total_meeting_data, create_type_meeting_data, create_type_meeting_structure,
        create_sales_eng_data_structure,create_sep_eng_sales_data, create_product_data,
        create_product_structure, meeting_tracker, Utils} from './dataset_functions.js'
const data                     = JSON.parse(document.getElementById("data").textContent);
// const appointment_data         = JSON.parse(document.getElementById("appointment_data").textContent);
// const product_name_list        = JSON.parse(document.getElementById("products").textContent);
// const sales_reps               = JSON.parse(document.getElementById("sales_reps").textContent);
// const appointment_type_names   = JSON.parse(document.getElementById('appointment_type_names').textContent);
const product_meeting_chart    = document.getElementById("product-chart").getContext('2d');
const total_meeting_chart      = document.getElementById("meeting-chart").getContext('2d');
const type_meeting_chart       = document.getElementById('type-meeting-chart').getContext('2d');
const sales_rep_meeting_chart  = document.getElementById('sales-rep-meeting-chart').getContext('2d');
console.log(data)

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
    dataset['product_data']   = [...create_product_data(product_names)];

    return dataset;
}

 const chart_data = create_meeting_data()
//
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
//
//
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
