def solution_decoder(assignments, sequence_positions, wor_orders):
    positions = sorted(enumerate(sequence_positions), key=lambda x: x[1])

    schedule = [[] for i in range(max(assignments) + 1)]
    #for wo_idx in range(len(assignments)):
    #    technician = assignments[wo_idx]
    #    schedule[technician].append(wor_orders[wo_idx])
    for wo_idx, _ in positions:
        technician = assignments[wo_idx]
        schedule[technician].append(wor_orders[wo_idx])

    for technician_schedule in schedule:
        current_time = 0
        prev_wo = None
        for work_order in technician_schedule:
            if prev_wo:
                current_time += get_travel_time(prev_wo, work_order)
            current_time += work_order.processing_time
            work_order.starting_time = current_time
            prev_wo = work_order
    
    return schedule

def starting_time(schedule):
        twc = 0
        for technician_schedule in schedule:
            current_time = 0
            prev_wo = None
            for work_order in technician_schedule:
                if prev_wo:
                    current_time += get_travel_time(prev_wo, work_order)
                current_time += work_order.processing_time
                work_order.starting_time = current_time
                prev_wo = work_order
        return twc

def get_travel_time(wo1,wo2):
    return 0