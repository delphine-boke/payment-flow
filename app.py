# app.py
# flask app for payment and reconciliation workflow with multiple currencies

# will be considering these countries:
# kenya, uganda, tanzania, rwanda, south africa and nigeria
# and the usd and euro ones.

from flask import Flask, request, render_template
import pandas as pd
from io import StringIO

app = Flask(__name__)

# sample ledger for reconciliation (in-memory, amounts in usd)
ledger = pd.DataFrame({
    'transaction_id': ['TXN001', 'TXN002', 'TXN003'],
    'amount': [100.00, 200.00, 150.00],  # amounts in usd
    'currency': ['USD', 'USD', 'USD'],
    'recipient': ['SupplierA', 'SupplierB', 'SupplierC'],
    'date': ['2025-06-27', '2025-06-27', '2025-06-27']
})

# fixed fx rates (currency to usd)
# no external apis
fx_rate = {
    'USD': 1.0,
    'EUR': 1.06,
    'KES': 128.95,
    'TZS': 2703.00,
    'RWF': 1363.15,
    'NGN': 1650.00,
    'ZAR': 18.12
}

@app.route('/')
def home():
    # render upload form
    # return render_template('index.html')
    return render_template('index.html', fx_rate=fx_rate)    

@app.route('/upload', methods=['POST'])
def upload():
    # handle csv upload
    file = request.files['file']
    if not file:
        return "No file uploaded", 400
    
    # read csv
    data = pd.read_csv(file)
    
    # validate csv columns
    required_columns = ['transaction_id', 'amount', 'currency', 'recipient', 'date']
    if not all(col in data.columns for col in required_columns):
        return "Invalid CSV format", 400
    
    # validate currency
    if not all(data['currency'].isin(fx_rate.keys())):
        return "Invalid currency in CSV", 400
    
    # convert amounts to usd for reconciliation
    data['amount_usd'] = data.apply(
        lambda x: x['amount'] / fx_rate[x['currency']], axis=1
    )
    
    # reconcile with ledger
    merged = data.merge(
        ledger, 
        on=['transaction_id', 'recipient'], 
        how='left', 
        suffixes=('_input', '_ledger')
    )
    
    # check for matches
    merged['status'] = merged.apply(
        lambda x: 'Matched' if abs(x['amount_usd'] - x['amount_ledger']) < 0.01 else 'Unmatched',
        axis=1
    )
    
    # prepare results
    results = merged[[
        'transaction_id', 'amount_input', 'currency_input', 
        'recipient', 'date_input', 'status'
    ]].to_dict(orient='records')
    
    # return render_template('results.html', results=results)
    return render_template('results.html', results=results, show_results=True)

if __name__ == '__main__':
    app.run(debug=True)
    
    