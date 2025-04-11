from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class WorkOrder:
    id: int
    processing_time: int
    breakdown: bool
    priority: str
    eligible_techs: int
    last_inspection_date: str
    starting_time: int = None

    def _get_due_date(self):
        date = datetime.strptime(self.last_inspection_date, '%Y-%m-%d')
        due_date = date + timedelta(days=30)
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