from datetime import datetime



def sales_date():
    today = datetime.today()

    time  = {
        'start' : {
           'year'  : 0,
           'month' : 0,
           'day'   : 22,
        },
        'stop': {
            'year' : 0,
            'month': 0,
            'day'  : 21,
        },

    }


    if (today.month - 1) > 0:
        time['start']['month'] = today.month
        time['stop'] ['month'] = today.month + 1
        time['start']['year']  = today.year
        time['stop']['year']   = today.year


    else:
        time['start']['month'] = 12
        time['stop']['month']  = today.month
        time['start']['year']  = today.year - 1
        time['stop']['year']   = today.year


    return time
