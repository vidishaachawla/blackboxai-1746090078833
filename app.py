from flask import Flask, request, jsonify, send_from_directory, redirect
from datetime import datetime, timedelta
import random

app = Flask(__name__, static_folder='static')

def get_mock_market_indicators():
    # Mock data for market indicators
    return {
        "overall_trend": random.choice(["bullish", "bearish"]),
        "us_futures_direction": random.choice(["up", "down"]),
        "european_markets_direction": random.choice(["up", "down"]),
        "volatility_index": round(random.uniform(15, 30), 2),
        "risk_assessment": random.choice(["low", "medium", "high"])
    }

def calculate_confidence_score(indicators):
    score = 0
    if indicators["overall_trend"] == "bullish":
        score += 30
    if indicators["us_futures_direction"] == "up":
        score += 25
    if indicators["european_markets_direction"] == "up":
        score += 25
    if indicators["volatility_index"] < 20:
        score += 20
    return min(score, 100)

def get_indian_stock_data(symbol):
    # Mock current price
    current_price = round(random.uniform(100, 1500), 2)
    # Mock prediction logic using market indicators
    indicators = get_mock_market_indicators()
    confidence = calculate_confidence_score(indicators)

    # Predicted price change based on confidence and random factor
    price_change_percent = round(random.uniform(-2, 2) * (confidence / 100), 2)
    predicted_price = round(current_price * (1 + price_change_percent / 100), 2)
    price_change_dollars = round(predicted_price - current_price, 2)

    # Next day's market close time (assume next weekday 3:30 PM IST)
    now = datetime.utcnow()
    next_day = now + timedelta(days=1)
    target_time = next_day.replace(hour=9, minute=0, second=0, microsecond=0)  # 9 AM UTC ~ 3:30 PM IST

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "predicted_closing_price": predicted_price,
        "price_change_dollars": price_change_dollars,
        "price_change_percent": price_change_percent,
        "confidence_score": confidence,
        "target_time": target_time.isoformat() + "Z",
        "market_indicators": indicators
    }

@app.route('/')
def index():
    return redirect('/real-time-stocks')

@app.route('/api/stock-prediction', methods=['GET'])
def stock_prediction():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Missing stock symbol"}), 400
    data = get_indian_stock_data(symbol)
    return jsonify(data)

@app.route('/real-time-stocks')
def serve_realtime_stocks():
    return send_from_directory('static', 'RealTimeStocks.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
