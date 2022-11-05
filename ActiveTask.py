class ActiveTask:
    def __init__(self,issue_description, issue_id, issue_reported_on, issue_type, priority, vehicle_id, vehicle_type):
      self.issue_description = issue_description
      self.issue_id = issue_id
      self.issue_reported_on = issue_reported_on
      self.issue_type = issue_type
      self.priority = priority
      self.vehicle_id = vehicle_id
      self.vehicle_type = vehicle_type

    def printname(self):
        print(self.issue_description, self.issue_id)

    def to_json(self):
        return {"Issue": {'issue_description': self.issue_description,
                               'issue_id': self.issue_id,
                               'issue_reported_on': self.issue_reported_on,
                               'issue_type': self.issue_type,
                               'priority': self.priority,
                               'vehicle_id': self.vehicle_id,
                               'vehicle_type': self.vehicle_type,}}
                               