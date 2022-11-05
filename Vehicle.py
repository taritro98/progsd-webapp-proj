class Vehicle:
    def __init__(self, vehicle_number, vehicle_type, last_used_on, percentage_of_charge, ride_kms):
      self.vehicle_number = vehicle_number
      self.vehicle_type = vehicle_type
      self.last_used_on = last_used_on
      self.percentage_of_charge = percentage_of_charge
      self.ride_kms = ride_kms

    def printname(self):
        print(self.vehicle_number, self.vehicle_type)

    def to_json(self):
        return {"Vehicle": {"vehicle_number": self.vehicle_number,
                          "vehicle_type": self.vehicle_type,
                          "last_used_on": self.last_used_on,
                          "percentage_of_charge": self.percentage_of_charge,
                          "ride_kms": self.ride_kms}}
