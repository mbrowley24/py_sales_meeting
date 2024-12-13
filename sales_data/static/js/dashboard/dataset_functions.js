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

const sales_eng_list = (sales_eng_mgr_names) =>{

    const data            = {}
    const mgr             = Object.keys(sales_eng_mgr_names)[0]
    const sales_eng_names = Object.keys(sales_eng_mgr_names[mgr])

    for(let i = 0; i < sales_eng_names.length; i++){

        const sales_rep_structure     = JSON.parse(JSON.stringify(sales_eng_mgr_names[mgr][sales_eng_names[i]]));

        const sales_rep_keys          = Object.keys(sales_rep_structure);

        for(let j = 0; j < sales_rep_keys.length; j++){

            const appointment_list    = [...sales_rep_structure[sales_rep_keys[j]]];

            for(let k = 0; k < appointment_list.length; k++){

                console.log(appointment_list[k])

            }
        }
    }
}


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
export const create_product_structure = (json_data) =>{

    console.log(json_data)

    const product_names = [...json_data['products']];
    const mgr             = Object.keys(json_data['sales_eng_mgr'])[0]
    const sales_eng_names = Object.keys(json_data['sales_eng_mgr'][mgr])

    const data = {}

    for(let i = 0; i < product_names.length; i++){

        if(data[product_names]){
           continue;
        }

        data[product_names[i]] = Array(12).fill(0);
    }

    for(let i = 0; i < sales_eng_names.length; i++){

        const sales_rep_structure     = JSON.parse(JSON.stringify(json_data['sales_eng_mgr'][mgr][sales_eng_names[i]]));

        const sales_rep_keys          = Object.keys(sales_rep_structure);

        for(let j = 0; j < sales_rep_keys.length; j++){

            const appointment_list    = [...sales_rep_structure[sales_rep_keys[j]]];

            for(let k = 0; k < appointment_list.length; k++){

                const appointment = JSON.parse(JSON.stringify(appointment_list[k]))
                console.log(appointment)

                const products    = [...appointment.products];

                for(let l = 0; l < products.length; l++){

                    const product = JSON.parse(JSON.stringify(products[l]))

                    console.log(product)
                    const month = new Date(appointment.date).getMonth();

                    data[product][month]++

                }

            }
        }
    }




    return data;
}

//create sales rep structure
export const create_sales_eng_data_structure = (names) =>{

    const data = {}
    const mgr  = Object.keys(names)[0]
    const sales_eng_names = Object.keys(names[mgr])


    for(let i = 0; i < sales_eng_names.length; i++){

        data[sales_eng_names[i]] = Array(12).fill(0);

        const sales_reps     = JSON.parse(JSON.stringify(names[mgr][sales_eng_names[i]]))
        const sales_rep_keys = Object.keys(sales_reps);

        for(let j = 0; j < sales_rep_keys.length; j++){

            const appointment = [...sales_reps[sales_rep_keys[j]]];

            for(let k = 0; k < appointment.length; k++){

                const date = new Date(appointment[k].date);

                data[sales_eng_names[i]][date.getMonth()] = data[sales_eng_names[i]][date.getMonth()] + 1

            }

        }

    }
    return data;
}


//create meeting type map
export const create_type_meeting_structure = (json_data) =>{

    console.log(json_data)

    const data            = {};
    const mgr             = Object.keys(json_data['sales_eng_mgr'])[0]
    const sales_eng_names = Object.keys(json_data['sales_eng_mgr'][mgr])
    const types           = [...json_data['meeting_types']];

    for(let i = 0; i < types.length; i++){

        data[types[i]] = Array(12).fill(0);
    }


    for(let i = 0; i < sales_eng_names.length; i++){

        console.log(sales_eng_names[i]);
        const sales_eng_structure     = JSON.parse(JSON.stringify(json_data['sales_eng_mgr'][mgr][sales_eng_names[i]]));

        const sales_eng_keys          = Object.keys(sales_eng_structure);

        for(let j = 0; j < sales_eng_keys.length; j++){

            const appointment_list    = [...sales_eng_structure[sales_eng_keys[j]]];

            for(let k = 0; k < appointment_list.length; k++){

                const appointment = JSON.parse(JSON.stringify(appointment_list[k]))
                const month = new Date(appointment.date).getMonth();

                data[appointment.type][month]++

            }
        }
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
    console.log(type_meetings)
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
export const create_sep_eng_sales_data = (sales_rep_data) =>{
    const data_set       = []

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


export const meeting_tracker = (sales_eng_mgr_names) =>{

    const data            = Array(12).fill(0);
    const mgr             = Object.keys(sales_eng_mgr_names)[0]
    const sales_eng_names = Object.keys(sales_eng_mgr_names[mgr])

    for(let i = 0; i < sales_eng_names.length; i++){

        const sales_rep_structure     = JSON.parse(JSON.stringify(sales_eng_mgr_names[mgr][sales_eng_names[i]]));

        const sales_rep_keys          = Object.keys(sales_rep_structure);

        for(let j = 0; j < sales_rep_keys.length; j++){

            const appointment_list    = [...sales_rep_structure[sales_rep_keys[j]]];

            for(let k = 0; k < appointment_list.length; k++){

                const date            = new Date(appointment_list[k].date)


                data[date.getMonth()] = data[date.getMonth()] + 1

            }
        }
    }
    return data;
}