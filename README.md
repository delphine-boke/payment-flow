# Finance Workflows
A B2B fintech tool to streamline payment processing and reconciliation for African businesses.

## Features

Upload CSV files with transaction data (transaction_id, amount, currency, recipient, date).

Supports currencies: KES, TZS, RWF, NGN, ZAR, USD, EUR with fixed FX conversion to USD.

Reconciles transactions against a sample ledger with Matched/Unmatched status.

Single-page interface with Home, About, Countries Supported, Contact, and Results sections.

## Prerequisites

Python 3.x

Required packages: flask, pandas

## Installation

Clone the repository or create a directory 

Navigate to the directory


Create a virtual environment


Install dependencies:pip install flask pandas


## Usage

Run the app:python app.py


Open your browser and go to http://127.0.0.1:5000.

Upload a CSV file with the required columns to see reconciliation results.

## Sample CSV
Create a file named transactions.csv with:
transaction_id,amount,currency,recipient,date
TXN001,12895,KES,SupplierA,2025-06-27
TXN002,200,USD,SupplierB,2025-06-27

## Contributing
Feel free to submit issues or pull requests for improvements.

## License

© 2025 Finance Workflows. All rights reserved.