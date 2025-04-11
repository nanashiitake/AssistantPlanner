from pymoo.core.problem import Problem
from pymoo.core.repair import Repair
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from src.workorder_class import WorkOrder
from src.decoding import solution_decoder
from typing import List
import numpy as np
import pandas as pd
from ast import literal_eval


class technicianEligibility(Repair):
    def __init__(self, work_orders):
        super().__init__()
        self.n_jobs = len(work_orders)
        self.work_orders = work_orders
    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            technician_assignments = X[i][::2]
            for j in range(self.n_jobs):
                if  int(technician_assignments[j]) not in self.work_orders[j].eligible_techs:
                    choice = np.random.choice(list(self.work_orders[j].eligible_techs))
                    X[i][j*2] = int(choice)
        return X


class assistantPlanner(Problem):
    def __init__(self, n_technicians: int, work_orders: List[WorkOrder], travel_times: np.ndarray):
        self.n_technicians = n_technicians
        self.work_orders = work_orders
        self.n_work_orders = len(work_orders)
        self.travel_times = travel_times
        self.n_var = self.n_work_orders*2
        self.n_obj = 1
        super().__init__(
            n_var=self.n_var,
            n_obj=self.n_obj, 
            n_ieq_constr=0,
            xl=np.zeros(self.n_work_orders*2),
            xu=np.column_stack([np.full(self.n_work_orders, self.n_technicians), np.ones(self.n_work_orders)]).flatten())
    def _evaluate(self, x, out, *args, **kwargs):
        F = np.zeros((x.shape[0], self.n_obj))
        G = np.zeros((x.shape[0], 0))
        

        for s_idx in range(x.shape[0]):
            # Interpretation de la solution
            technicians_assignments = x[s_idx][ ::2].astype(int)
            sequence_positions = x[s_idx][1::2]

            schedule = solution_decoder(technicians_assignments, sequence_positions, self.work_orders)
            F[s_idx,0] = self._weighted_completion_time(schedule)
            out["F"] = F
            #F[s_idx,1] = self._tardiness(schedule)
            #F[s_idx,2] = self._earliness(schedule)

    def _weighted_completion_time(self, schedule):
        twc = 0
        for technician_schedule in schedule:
            current_time = 0
            prev_wo = None
            for work_order in technician_schedule:
                if prev_wo:
                    current_time += get_travel_time(prev_wo, work_order)
                current_time += work_order.processing_time
                twc += work_order._get_weight() * current_time
                prev_wo = work_order
        return twc        

def get_travel_time(wo1,wo2):
    return 0


work_orders_df = pd.read_csv('data/jobs_df.csv', converters={'Required Skills': literal_eval, 'Eligibility': literal_eval})


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

work_orders = WorkOrders_from_df(work_orders_df)
technicians = pd.read_csv('data/tech_df.csv', converters={'MD_Skills': literal_eval})


problem = assistantPlanner(7, work_orders, travel_times=np.zeros((len(work_orders), len(work_orders))))

algorithm = NSGA2(
    pop_size=400,
    eliminate_duplicates=True,
    repair=technicianEligibility(work_orders)
)

res = minimize(
    problem,
    algorithm,
    ('n_gen', 100),
    verbose=True
)