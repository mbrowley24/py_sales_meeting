

def customer_table_transform(customer, sales_engineer):


    return{
        'name'           : customer.name,
        'vertical'       : customer.vertical.name,
        'sales_rep'      : f'{customer.sales_rep.first_name} {customer.sales_rep.last_name}',
        'sales_engineer' : f'{sales_engineer.first_name} {sales_engineer.last_name}',
        'appointments'   : customer.appointments.count()
    }