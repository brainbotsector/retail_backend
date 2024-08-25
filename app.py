from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load data from CSV
df = pd.read_csv('Product._Full Data_data (1).csv')


print(df.columns)

@app.route('/api/sales_by_location', methods=['GET'])
def sales_by_location():
    try:
        data = df.groupby('Country').agg({'sales': 'sum'}).sort_values(by='sales', ascending=False).head(10).reset_index()
        return jsonify(data.to_dict(orient='records'))
    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 500

@app.route('/api/top_sold_products', methods=['GET'])
def top_sold_products():
    try:
        data = df.groupby('Description').agg({'sales': 'sum'}).sort_values(by='sales', ascending=False).head(10).reset_index()
        return jsonify(data.to_dict(orient='records'))
    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 500

@app.route('/api/customer_details', methods=['GET'])
def customer_details():
    try:
        data = df[['Customer ID', 'Country', 'Latest purchase', 'No of Purchases', 'sales']].head(10)
        return jsonify(data.to_dict(orient='records'))
    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 500

@app.route('/api/daily_sales_trend', methods=['GET'])
def daily_sales_trend():
    try:
        data = df.groupby('Latest purchase').agg({'sales': 'sum'}).reset_index()
        return jsonify(data.to_dict(orient='records'))
    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
