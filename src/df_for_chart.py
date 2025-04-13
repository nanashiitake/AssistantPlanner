import pandas as pd
from operator import attrgetter
import plotly.express as px

def list_to_df(work_orders):
    df = pd.DataFrame({
        'id': [wo.id for wo in work_orders],
        'starting_time': [wo._get_real_starting_time() for wo in work_orders],
        'completion_time': [wo._get_real_completion() for wo in work_orders],
        'technician': [wo.assigned_tech.first_name for wo in work_orders],
        'breakdown': [wo.breakdown for wo in work_orders],
        'deadline': [wo._get_due_date() for wo in work_orders]
    })
    return df