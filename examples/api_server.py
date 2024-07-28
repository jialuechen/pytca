from flask import Flask, request, jsonify
from pytca.analysis.general.metrics import calculate_vwap

app = Flask(__name__)

@app.route('/vwap', methods=['POST'])
def vwap():
    try:
        data = request.json
        prices = data['prices']
        volumes = data['volumes']
        
        # Calculate VWAP
        vwap_value = calculate_vwap(prices, volumes)
        
        if vwap_value is None:
            return jsonify({"error": "Invalid input data"}), 400
        
        return jsonify({"vwap": vwap_value})
    except KeyError as e:
        return jsonify({"error": f"Missing key in input data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

