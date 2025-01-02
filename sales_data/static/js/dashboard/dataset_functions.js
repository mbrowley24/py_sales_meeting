console.log('dataset functions loaded');


//utils to create month label
export const Utils = {
  months: ({ count }) => Array.from({ length: count }, (_, i) => new Date(0, i).toLocaleString('en', { month: 'long' }))
};


export const colors = [
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

const get_sales_eng_team = (json_data, name) =>{

    return json_data['sales_engineer_teams'].filter(mgr => mgr.name === name)[0]['engineers'];
}


export const sales_eng_mgr_name_list = (json_data) =>{

    const name_list = [];

    for(let i = 0; i < json_data.length; i++){

        name_list.push(json_data[i].name)
    }


    return name_list;
}

export const sales_eng_meeting_totals = (json_data, name) =>{

    const months                 = Utils.months({'count' : 12})
    const sales_eng_meeting_list = {
        total_meetings_charts  : [],
        sales_eng_names        : [],
        meetings               : [],
    };

    const sales_eng_team         = get_sales_eng_team(json_data, name);


    for(let i = 0; i < sales_eng_team.length; i++){

        const sales_eng_name = sales_eng_team[i].name
        
        sales_eng_meeting_list['sales_eng_names'].push(sales_eng_name);
        
        const sales_reps = [...sales_eng_team[i]['sales_reps']]

        for(let j = 0; j < sales_reps.length; j++){

            const meetings = [...sales_reps[j]['appointments']];

            for(let k = 0; k < meetings.length; k++){

                const month = months[k];
                const meeting_count = meetings[k];

                let found = false;

                for(let l = 0; l < sales_eng_meeting_list['meetings'].length; l++){

                    const name_match = sales_eng_meeting_list['meetings'][l].name  === sales_eng_name;
                    const month_name = sales_eng_meeting_list['meetings'][l].month === month;

                    if(name_match && month_name){
                        sales_eng_meeting_list['meetings'][l].meetings += meeting_count;

                        found = true;
                        break;
                    }
                }

                if(!found){

                    sales_eng_meeting_list['meetings'].push({
                        'name'     : sales_eng_name,
                        'month'    : month,
                        'meetings' : meeting_count,
                    });
                }
            }
        }

    }

    return sales_eng_meeting_list

}


export const meeting_types = (json_data, name) =>{

    const months                 = Utils.months({'count' : 12})
    const sales_eng_meeting_list = {
        sales_eng_names : [],
        meetings        : [],
    };

    const sales_eng_team         = get_sales_eng_team(json_data, name);


}






