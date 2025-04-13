#%%
from pymoo.core.problem import Problem
from pymoo.core.repair import Repair
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

from src.decoding import solution_decoder
from src.classes import WorkOrder, Technician
from src.lists import technicians, work_orders
from src.best_solution import get_best_solution
from src.df_for_chart import list_to_df

from typing import List
import numpy as np
import pandas as pd
from ast import literal_eval
import plotly.express as px


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
    def __init__(self, n_technicians: int, work_orders: List[WorkOrder], travel_times: np.ndarray, technicians: List[Technician]):
        self.n_technicians = n_technicians
        self.work_orders = work_orders
        self.n_work_orders = len(work_orders)
        self.travel_times = travel_times
        self.n_var = self.n_work_orders*2
        self.n_obj = 1
        self.technicians = technicians
        super().__init__(
            n_var=self.n_var,
            n_obj=self.n_obj, 
            n_ieq_constr=1,
            xl=np.zeros(self.n_work_orders*2),
            xu=np.column_stack([np.full(self.n_work_orders, self.n_technicians), np.ones(self.n_work_orders)]).flatten())
    def _evaluate(self, x, out, *args, **kwargs):
        F = np.zeros((x.shape[0], self.n_obj))
        G1 = np.zeros((x.shape[0], self.n_obj))
        G2 = np.zeros((x.shape[0], self.n_obj))
        G = np.zeros((x.shape[0], self.n_obj))
        

        for s_idx in range(x.shape[0]):
            # Interpretation de la solution
            technicians_assignments = x[s_idx][ ::2].astype(int)
            sequence_positions = x[s_idx][1::2]

            schedule = solution_decoder(technicians_assignments, sequence_positions, self.work_orders, self.technicians)
            F[s_idx,0] = self._weighted_completion_time()
            G[s_idx,0] = self._tardiness()
            #G2[s_idx,0] = self._earliness()
            #G = np.column_stack([G1, G2])
            out["F"] = F
            out["G"] = [G]
            #out["G1"] = G1
            #F[s_idx,1] = self._tardiness(schedule)
            #F[s_idx,2] = self._earliness(schedule)

    def _weighted_completion_time(self):
        twc = sum(work_order._get_weighted_completion_time() for work_order in work_orders)
        return twc
    #def _tardiness(self):
    #    tardiness = sum(work_order._get_tardiness() for work_order in work_orders)
    def _tardiness(self):
        tardiness = 0
        for work_order in work_orders:
            if type(work_order._get_due_date()) != type(None):
                tardiness += work_order._get_tardiness()
        return tardiness 
            

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

#work_orders = WorkOrders_from_df(work_orders_df)
#technicians = pd.read_csv('data/tech_df.csv', converters={'MD_Skills': literal_eval})


problem = assistantPlanner(7, work_orders, travel_times=np.zeros((len(work_orders), len(work_orders))), technicians=technicians)

algorithm = NSGA2(
    pop_size=200,
    eliminate_duplicates=True,
    repair=technicianEligibility(work_orders)
)

res = minimize(ConstraintsAsPenalty(problem, penalty=10),
    ##ConstraintsAsObjective(problem), 
    algorithm,
    ('n_gen', 300),
    verbose=True
)

best_x, best_f = get_best_solution(res)
solution = solution_decoder(best_x[::2].astype(int), best_x[1::2], work_orders, technicians)


df = list_to_df(work_orders)

fig1 = px.timeline(df, x_start="starting_time", x_end="completion_time", y="technician", color='breakdown', text='id', hover_data=['deadline'], range_x=['2024-11-04', '2024-11-09'])
fig1.show()
# %%
