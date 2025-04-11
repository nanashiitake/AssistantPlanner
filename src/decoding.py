def solution_decoder(assignments, sequence_positions, wor_orders):
    sorted_sequence = sorted(enumerate(sequence_positions), key=lambda x: x[1])

    schedule = [[] for i in range(max(assignments) + 1)]
    for wo_idx in range(len(assignments)):
        technician = assignments[wo_idx]
        schedule[technician].append(wor_orders[wo_idx])
    return schedule
