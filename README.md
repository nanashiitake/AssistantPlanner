# Assistant Planner
Solving a scheduling problem using Pymoo.
## Problem Definition
### Parallel Machines Scheduling problem:

- Non-preemptive: Jobs cannot be interrupted and resumed.
- Identical Machines: The job processing times are independent of the machines.
- Sequential Setup Times: the setup times are sequence dependent.
- Machine eligibilty constraints: Jobs can only be assigned to specific machines.
- Machine availability constraints: Machines have working shifts

### Objective Function

We will use the Total Weighted Completion time as our onbjective function

### Constraints

We will use pymoo's Constraint Violation as penalty feature to try to respect job's deadlines.

$C_t = S_t + P_t$
$C_t - Deadline \le 0$
