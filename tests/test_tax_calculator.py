import unittest

from src.tax_calculator import TaxCalculator


class TestTaxCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = TaxCalculator('config/tax_rules.json')

    def test_chargeable_times(self):
        tests = [
            ('06:15:00', 8),
            ('07:45:00', 18),
            ('15:15:00', 13),
            ('17:45:00', 13),
            ('18:15:00', 8),
            ('23:00:00', 0)
        ]
        for entry_time, expected in tests:
            self.assertEqual(self.calculator._calculate_entry_tax(entry_time), expected)

    def test_exempt_vehicles(self):
        exempt_vehicles = [
            'Emergency vehicles',
            'Busses',
            'Diplomat vehicles',
            'Motorcycles',
            'Military vehicles',
            'Foreign vehicles'
        ]
        for vehicle in exempt_vehicles:
            self.assertTrue(self.calculator._is_vehicle_exempt(vehicle))

    def test_single_charge_rule(self):
        entry_times = [
            '06:15:00',
            '07:45:00',
            '08:15:00'
        ]
        self.assertEqual(len(self.calculator._apply_single_charge_rule(entry_times)), 1)

    def test_maximum_daily_charge(self):
        entry_times = [
            '06:15:00',
            '07:45:00',
            '08:15:00',
            '15:15:00',
            '17:45:00'
        ]
        self.assertEqual(self.calculator.calculate_tax('Car', entry_times), 60)

    def test_edge_cases(self):
        tests = [
            ('05:59:59', 0),
            ('06:00:00', 8),
            ('18:29:59', 8),
            ('18:30:00', 0)
        ]
        for entry_time, expected in tests:
            self.assertEqual(self.calculator._calculate_entry_tax(entry_time), expected)

if __name__ == '__main__':
    unittest.main()
