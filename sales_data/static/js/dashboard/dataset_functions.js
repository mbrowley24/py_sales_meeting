console.log('dataset functions loaded');


//utils to create month label
export const Utils = {
  months: ({ count }) => Array.from({ length: count }, (_, i) => new Date(0, i).toLocaleString('en', { month: 'long' }))
};




const colors = [
  'rgba(231, 76, 60, 0.8)',   'rgba(41, 128, 185, 0.8)',  'rgba(241, 196, 15, 0.8)',
  'rgba(39, 174, 96, 0.8)',   'rgba(155, 89, 182, 0.8)',  'rgba(236, 112, 99, 0.8)',
  'rgba(26, 188, 156, 0.8)',  'rgba(149, 165, 166, 0.8)', 'rgba(243, 156, 18, 0.8)',
  'rgba(241, 180, 15, 0.8)',  'rgba(255, 127, 80, 0.8)',  'rgba(65, 105, 225, 0.8)',
  'rgba(0, 255, 127, 0.8)',   'rgba(0, 191, 255, 0.8)',   'rgba(220, 20, 60, 0.8)',
  'rgba(175, 238, 238, 0.8)', 'rgba(176, 196, 222, 0.8)', 'rgba(218, 165, 32, 0.8)',
  'rgba(178, 34, 34, 0.8)',   'rgba(112, 128, 144, 0.8)', 'rgba(72, 201, 176, 0.8)',
  'rgba(0, 123, 255, 0.8)',   'rgba(255, 159, 243, 0.8)', 'rgba(255, 87, 34, 0.8)',
  'rgba(140, 122, 230, 0.8)', 'rgba(52, 152, 219, 0.8)',  'rgba(88, 214, 141, 0.8)',
  'rgba(230, 126, 34, 0.8)',  'rgba(241, 148, 138, 0.8)', 'rgba(46, 134, 193, 0.8)',
  'rgba(244, 208, 63, 0.8)',  'rgba(125, 60, 152, 0.8)',  'rgba(93, 173, 226, 0.8)',
  'rgba(203, 67, 53, 0.8)',   'rgba(82, 190, 128, 0.8)',  'rgba(244, 162, 97, 0.8)',
  'rgba(121, 134, 203, 0.8)', 'rgba(252, 243, 207, 0.8)', 'rgba(133, 193, 233, 0.8)',
  'rgba(174, 214, 241, 0.8)'
];



//create_total_meeting_line create line for total meetings for the given period
export const create_total_meeting_data = (total_meetings) =>{
    const dataset  = []

    dataset.push({
        label : "Meetings",
        data  : [...total_meetings],
        borderColor: 'rgba(0, 0, 0, 0.8)',
        borderWidth: 2,
        fill: false,
        tension: 0.1
    });

    return dataset;
}

//create product name map
export const create_product_structure = (product_names) =>{
    const data = {}

    for(let i = 0; i < product_names.length; i++){

        if(data[product_names]){
           continue;
        }

        data[product_names[i]] = Array(12).fill(0);
    }


    return data;
}

//create sales rep structure
export const create_sales_reps_data_structure = (names) =>{
    const data = {}

    for(let i = 0; i < names.length; i++){

        data[names[i]] = Array(12).fill(0);
    }

    return data;
}

//create meeting type map
export const create_type_meeting_structure = (types) =>{

    const data = {};

    for(let i = 0; i < types.length; i++){

        data[types[i]] = Array(12).fill(0);
    }

    return data;
}

export const create_product_data = (products) =>{
    const dataset = []
    const keys = Object.keys(products)

    for(let i = 0; i < keys.length; i++){

        const data = {
            label       : keys[i]?.toUpperCase(),
            data        : [...products[keys[i]]],
            borderColor : colors[i],
            borderWidth : 2,
            fill        : false
        }

        dataset.push(data)
    }


    return dataset
}

//create_type_meeting_data_structure for graph
export const create_type_meeting_data = (type_meetings) =>{

    const dataset = [];

    const keys = Object.keys(type_meetings)

    for(let i = 0; i < keys.length; i++){

        const data = {
            label       : keys[i]?.toUpperCase(),
            data        : [...type_meetings[keys[i]]],
            borderColor : colors[i],
            borderWidth : 2,
            fill        : false
        }

        dataset.push(data);

    }

    return dataset;
}



//create data points for sales reps and return an array
export const create_sep_rep_sales_data = (sales_rep_data) =>{
    const data_set       = []
    console.log(sales_rep_data)
    const keys = Object.keys(sales_rep_data)

    for(let i = 0; i < keys.length; i++){

        const data = {
            label       : keys[i]?.toUpperCase(),
            data        : [...sales_rep_data[keys[i]]],
            borderColor : colors[i],
            borderWidth : 2,
            fill        : false
        }

        data_set.push(data)
    }

    return data_set;
}
