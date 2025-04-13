from datetime import datetime, time, timedelta
def solution_decoder(assignments, sequence_positions, wor_orders, technicians):
    positions = sorted(enumerate(sequence_positions), key=lambda x: x[1])

    schedule = [[] for i in range(max(assignments) + 1)]
    for wo_idx, _ in positions:
        technician = assignments[wo_idx]
        wor_orders[wo_idx].assigned_tech = technicians[technician]
        schedule[technician].append(wor_orders[wo_idx])

    for technician_schedule in schedule:
        current_time = 0
        prev_wo = None
        for work_order in technician_schedule:
            if prev_wo:
                current_time += get_travel_time(prev_wo, work_order)
                current_time += prev_wo.processing_time
            work_order.starting_time = current_time
            work_order.starting_time = check_schedule(work_order)
            current_time = check_schedule(work_order)
            prev_wo = work_order
    
    return schedule

def get_travel_time(wo1,wo2):
    return 0

def check_schedule(work_order):
    start_time1 = time(7,0)
    end_time2 = time(17,0)
    completion = work_order._get_real_completion()
    if completion.time() > end_time2:
        return work_order.starting_time + (14*60 - time_difference(end_time2, work_order._get_real_starting_time().time()).total_seconds() / 60)
    
    if work_order._get_real_starting_time().time() < start_time1:
        return work_order.starting_time + time_difference(work_order._get_real_starting_time().time(), start_time1).total_seconds() / 60
    return work_order.starting_time

def time_difference(time1, time2):
    dt1 = datetime.combine(datetime.min, time1)
    dt2 = datetime.combine(datetime.min, time2)
    return dt2 - dt1