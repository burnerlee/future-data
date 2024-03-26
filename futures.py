from flask import Flask, jsonify, request
from nselib import derivatives

def get_nearest_expiry():
    expiries = derivatives.expiry_dates_future()
    return expiries[0]

def get_symbol_prices(symbol, expiry):
    data = derivatives.future_price_volume_data(
        symbol,
        "FUTSTK",
        period="1D",
    )
    print(f"found ${len(data)} records")
    for row in data.iterrows():
        if row[1]["EXPIRY_DT"] == expiry:
            return {
                "open": row[1]["OPENING_PRICE"],
                "high": row[1]["TRADE_HIGH_PRICE"],
                "low": row[1]["TRADE_LOW_PRICE"],
                "close": row[1]["CLOSING_PRICE"],
                "ltp": row[1]["LAST_TRADED_PRICE"],
            }

# data = get_symbol_prices("RELIANCE", get_nearest_expiry())
# print(data)

app = Flask(__name__)

@app.route("/get_future_data", methods=['GET'])
def get_future_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Missing symbol parameter'}), 400
    
    price_type = request.args.get('price_type', 'ltp')
    
    stock_data = get_symbol_prices(symbol, get_nearest_expiry())
    data = {
        "price": stock_data[price_type]
    }

    return jsonify(data)

@app.route("/", methods=['GET'])
def ping():
    return "Pong"

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

nearest_expiry = get_nearest_expiry()
stock_data = get_symbol_prices("AARTIIND", nearest_expiry)
print(stock_data)