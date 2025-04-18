from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Technician:
    id: int
    first_name: str
    last_name: str
    skill: int

@dataclass
class WorkOrder:
    id: int
    processing_time: int
    breakdown: bool
    priority: str
    eligible_techs: int
    last_inspection_date: str = None
    starting_time: int = None
    assigned_tech: int = None

    def _get_due_date(self):
        if type(self.last_inspection_date) == str:
            date = datetime.strptime(self.last_inspection_date, '%Y-%m-%d')
            date = date.replace(hour=12)
            due_date = date + timedelta(days=30)
        else:
            return None
        return(due_date)
    
    def _get_weight(self):
        if self.breakdown:
            return 18
        if self.priority == 'Very high':
            return 4
        if self.priority == 'High':
            return 3
        if self.priority == 'Medium':
            return 2
        if self.priority == 'Low':
            return 1
    
    def _get_weighted_completion_time(self):
        return (self.starting_time + self.processing_time) * self._get_weight()
    def _get_tardiness(self):
        if self.last_inspection_date != float('nan') and type(self._get_due_date) != type(None):
            real_completion_time = datetime.strptime('4/11/2024/07:00', '%d/%m/%Y/%H:%M') + timedelta(minutes= self.starting_time + self.processing_time)
            return abs((real_completion_time - self._get_due_date()).total_seconds() / 60)
        return None
    def _get_real_starting_time(self):
        return datetime.strptime('4/11/2024/07:00', '%d/%m/%Y/%H:%M') + timedelta(minutes= self.starting_time)
    def _get_real_completion(self):
        return datetime.strptime('4/11/2024/07:00', '%d/%m/%Y/%H:%M') + timedelta(minutes= self.starting_time + self.processing_time)