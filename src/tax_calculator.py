import datetime
import json


class TaxCalculator:
    def __init__(self, rules_path):
        self.tax_rules = self._load_tax_rules(rules_path)

    def _load_tax_rules(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def _is_vehicle_exempt(self, vehicle_type):
        return vehicle_type in self.tax_rules['exempt_vehicles']

    def _calculate_entry_tax(self, entry_time):
        for period, amount in self.tax_rules['tax_periods'].items():
            start, end = map(lambda t: datetime.datetime.strptime(t, "%H:%M").time(), period.split('–'))
            if start <= entry_time.time() <= end:
                return amount
        return 0

    def _apply_single_charge_rule(self, entry_times):
        entry_times.sort()
        charged_times = []
        for i, entry_time in enumerate(entry_times):
            if not charged_times or (entry_time - charged_times[-1]).seconds > 3600:
                charged_times.append(entry_time)
        return charged_times

    def calculate_tax(self, vehicle_type, entry_times):
        if self._is_vehicle_exempt(vehicle_type):
            return 0
        daily_tax = 0
        entry_times = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in entry_times]
        charged_times = self._apply_single_charge_rule(entry_times)
        for entry_time in charged_times:
            daily_tax += self._calculate_entry_tax(entry_time)
            if daily_tax >= self.tax_rules['max_daily_charge']:
                return self.tax_rules['max_daily_charge']
        return daily_tax
