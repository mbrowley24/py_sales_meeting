console.log("dashboard loaded")
import {get_sales_eng_names, Utils} from './dataset_functions.js';

const data                    = JSON.parse(document.getElementById("data").textContent);
const meeting_table_body      = document.getElementById('meeting_table_body');
const eng_name                = document.getElementById("eng_name");
const iah_col                 = document.getElementById("iah_count");
const pa_col                  = document.getElementById("pa_count");
const fa_col                  = document.getElementById("fa_count");
const product_eng             = document.getElementById("product_eng");
const type_eng                = document.getElementById("type_eng")

const product_meeting_chart   = document.getElementById("product-chart").getContext('2d');
const total_meeting_chart     = document.getElementById("meeting-chart");
const type_meeting_chart      = document.getElementById('type-meeting-chart').getContext('2d');
const sales_eng_meeting_chart = document.getElementById('sales-eng-meeting-chart');

//create labels
const labels = Utils.months({count: 12});
// const sales_eng_name_list      = sales_eng_list(data);


const dynamicFontSize = (container) =>{

    return Math.max(5, Math.min(container.offsetWidth / 50, 10));
}

const legendTextSize = (container) =>{
    // Calculate a dynamic percentage for the top position

    return Math.min(1, (container.offsetHeight * 0.02)) + '%'; // Example: Limit top to 10% max
}

console.log(data);
console.log(data['total_meetings'])

const create_meeting_data = () => {
    // const product_names       = create_product_structure(data, '');
    // const sales_end_meetings = create_sales_eng_data_structure(data['sales_eng_mgr']);


    const dataset = {
        product_data       : [],
        running_line_chart : [],
        sales_eng_names    : [],
        sales_mgr_names    : [],
        sales_rep_data     : [],
        type_meeting       : [],
        total_meetings     : [],
    }



    // dataset['sales_mgr_names']     = [...sales_eng_mgr_name_list(data['sales_engineer_teams'])];
    // const sales_eng_meetings       = sales_eng_meeting_totals(data, dataset['sales_mgr_names'][0])
    // dataset['sales_eng_names']     = [...sales_eng_meetings['sales_eng_names']]


    dataset['running_line_chart']  = [...sales_eng_meetings['meetings']];

    dataset['total_meetings']      = [...data['total_meetings']];




    return dataset;
}


// let   sales_eng_meeting_data  = create_meeting_table_body_data()
// const chart_data              = create_meeting_data();


//create_total_meeting_charts creates a total meeting chart
const create_total_meeting_charts = () => {

    const total_meetings = echarts.init(total_meeting_chart, null, {
        width  : total_meeting_chart.innerWidth,
        height : total_meeting_chart.innerHeight
    });

    const fontSize             = dynamicFontSize(sales_eng_meeting_chart);
    // const legendFrontSize      = legendTextSize(sales_eng_meeting_chart);

    const option = {
        xAxis: {
            type : 'category',
            data : labels,
            axisLabel    : {
                interval : 1,
                fontSize : fontSize,
                color    : 'black'
            },
            axisTick: {
                show : true,
                length: fontSize / 2, // Example: Adjust tick length dynamically
                lineStyle: {
                    width: fontSize / 10, // Example: Adjust tick width dynamically
                    color: 'black'       // Keep tick color consistent
                },
                interval : 1,
            },
        },
        yAxis: {
            // name: 'Meetings'
            axisLabel : {
                fontSize : fontSize,
                color    : 'black'
            },
        },
         series  : [{
            type   : 'line',
            data   : [...data['total_meetings']],
            smooth : true,
        }]
    };

    total_meetings.setOption(option);

    return total_meetings;
}

const total_meeting_chart_dynamic = (data_obj) =>{


    data_obj.element.setOption({

        xAxis: {
            type : 'category',
            data : labels,
            axisLabel    : {
                interval : 1,
                fontSize : data_obj.fontSize,
                color    : 'black'
            },
            axisTick: {
                show : true,
                length: data_obj.fontSize / 2, // Example: Adjust tick length dynamically
                lineStyle: {
                    width: data_obj.fontSize / 10, // Example: Adjust tick width dynamically
                    color: 'black'       // Keep tick color consistent
                },
                interval : 1,
            },
        },
        yAxis: {
            // name: 'Meetings'
            axisLabel : {
                fontSize : data_obj.fontSize,
                color    : 'black'
            },
        },
         series  : [{
            type   : 'line',
            data   : [...data['total_meetings']],
            smooth : true,
        }]
    });

    data.element.resize();


}

//create_sales_reps_meeting_number create chart for tracking for sales rep meeting
//also a function for dynamic resizing
const create_sales_eng_meeting_data = () => {

    const line_chart = echarts.init(sales_eng_meeting_chart , null, {
        width: sales_eng_meeting_chart.innerWidth,
        height: sales_eng_meeting_chart.innerHeight
    });

    console.log(get_sales_eng_names(data['sales_eng_meetings_chart']))

    const fontSize             = dynamicFontSize(sales_eng_meeting_chart);
    const legendFrontSize      = legendTextSize(sales_eng_meeting_chart);
    const sales_eng_names    = [...chart_data['sales_eng_names']]
    const datasetWithFilters = [];
    const seriesList         = [];

    // Build datasets and series
    echarts.util.each(sales_eng_names, function (eng) {
        const datasetId = 'dataset_' + eng;
        datasetWithFilters.push({
            id: datasetId,
            fromDatasetId: 'dataset_raw',
            transform: {
                type: 'filter',
                config: {
                    and: [
                        { dimension: 'eng', '=': eng } // Filter data by name
                    ]
                }
            }
        });

        seriesList.push({
            type: 'line', // Change to 'bar' if you prefer bar charts
            datasetId: datasetId,
            showSymbol: true,
            name: eng,
            encode: {
                x: 'month',   // X-axis is the month
                y: 'meetings' // Y-axis is the number of meetings
            },
            emphasis: {
                focus: 'series'
            }
        });
    });

    // Chart options
    const option = {
        animationDuration: 3000,
        dataset: [
            {
                id: 'dataset_raw',
                source: chart_data['running_line_chart'] // Use the provided data
            },
            ...datasetWithFilters
        ],
        // title: {
        //     text: 'Monthly Meetings by Sales Rep'
        // },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            top       : legendFrontSize,
            data      : sales_eng_names,
            formatter : function (name) {
                return name.length > 10 ? name.substring(0, 10) + '...' : name;
            },
            textStyle : {
                color    : 'black',
                fontSize : fontSize
            }
        },
        xAxis: {
            type         : 'category',
            nameLocation : 'middle',
            data         : [...data['months']],
            axisLabel    : {
                interval : 1,
                fontSize : fontSize,
                color    : 'black'
            },
            axisTick: {
                show : false,
                length: fontSize / 2, // Example: Adjust tick length dynamically
                lineStyle: {
                    width: fontSize / 10, // Example: Adjust tick width dynamically
                    color: 'black'       // Keep tick color consistent
                },
                interval : 1,
                //splitNumber : 2
            },

        },
        yAxis: {
            // name: 'Meetings'
            axisLabel : {
                fontSize : fontSize,
                color    : 'black'
            },

        },
        grid: {
            right : 140
        },
        series: seriesList
    };

    line_chart.setOption(option)


    return line_chart
};

const sales_eng_meeting_data_dynamic = (data) =>{

    // Update chart options with new font size
    data.element.setOption({
        legend: {
            top       : data.legendFrontSize,
            data      : data.sales_eng_names,
            formatter : function (name) {
                return name.length > 10 ? name.substring(0, 10) + '...' : name;
            },
            textStyle : {
                color    : 'black',
                fontSize : data.fontSize
            }
        },
        xAxis: {
            type         : 'category',
            nameLocation : 'middle',
            data         : [...Utils.months({'count' : 12})],
            axisLabel    : {
                interval : 1,
                fontSize : data.fontSize,
                color    : 'black'
            },
            axisTick: {
                show : true,
                length: data.fontSize / 2, // Example: Adjust tick length dynamically
                lineStyle: {
                    width: data.fontSize / 10, // Example: Adjust tick width dynamically
                    color: 'black'       // Keep tick color consistent
                },
                interval : 1,
            },
        },
        yAxis: {
            // name: 'Meetings'
            axisLabel : {
                fontSize : data.fontSize,
                color    : 'black'
            },
        },
    });

    data.element.resize();
}





// const sales_eng_line_chart  = create_sales_eng_meeting_data();
const total_meetings_chart  = create_total_meeting_charts();
const sales_eng_line_chart  = create_sales_eng_meeting_data();


// Attach resize event listener for responsiveness
window.addEventListener('resize', () => {

    const fontSize        = dynamicFontSize(sales_eng_meeting_chart);
    const legendFrontSize = legendTextSize(sales_eng_meeting_chart);

    const sales_eng_sales_line_chart = {
        fontSize        : fontSize,
        legendFrontSize : legendFrontSize,
        element         : sales_eng_line_chart
    }

    sales_eng_meeting_data_dynamic(sales_eng_sales_line_chart)

    const total_meeting_chart = {
        fontSize        : fontSize,
        legendFrontSize : legendFrontSize,
        element         : total_meetings_chart
    }

    total_meeting_chart_dynamic(total_meeting_chart)


});
