import src.tax_calculator as tax_calculator
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/calculate_tax', methods=['POST'])
def calculate_tax():
    data = request.get_json()
    vehicle_type = data.get('vehicle_type')
    entry_times = data.get('entry_times')
    calculated_tax = tax_calculator.calculate_tax(vehicle_type, entry_times)
    return jsonify({"calculated_tax": calculated_tax})

if __name__ == '__main__':
    app.run(debug=True)
