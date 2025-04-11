import pandas as pd
from src.classes import WorkOrder, Technician
from ast import literal_eval

work_orders_df = pd.read_csv('data/jobs_df.csv', converters={'Required Skills': literal_eval, 'Eligibility': literal_eval})
technicians_df = pd.read_csv('data/tech_df.csv', converters={'MD_Skills': literal_eval})

def WorkOrders_from_df(df):
    workOrders = []
    for _, row in df.iterrows():
        work_order = WorkOrder(id=row['Work Order ID'],
                               processing_time=row['Processing Time'],
                               last_inspection_date=row['Last inspection date'],
                               priority=row['Priority'],
                               breakdown=row['Breakdown'] == 'Yes',
                               eligible_techs=set(row['Eligibility']))
        workOrders.append(work_order)
    return(workOrders)

def technicians_from_df(df):
    technicians = []
    for _, row in df.iterrows():
        technician = Technician(id=row['Technician ID'],
                                       first_name=row['Technician First Name'],
                                       last_name=row['Technician Last Name'],
                                       skill=row['MD_Skills'])
        technicians.append(technician)
    return technicians
technicians = technicians_from_df(technicians_df)
work_orders = WorkOrders_from_df(work_orders_df)

