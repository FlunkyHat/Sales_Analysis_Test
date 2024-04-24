from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the data
df = pd.read_csv('sales_data.csv')

# Preprocess the data
df['Call Date'] = pd.to_datetime(df['Call Date'])
df['Month'] = df['Call Date'].dt.month_name()
df['Value of sale'] = pd.to_numeric(df['Value of sale'], errors='coerce')
df = df.dropna(subset=['Value of sale'])

@app.route('/monthly_summary_data')
def monthly_summary_data():
    # Calculate the total sales value for each month
    monthly_summary = df.groupby('Month')['Value of sale'].sum().reset_index()

    # Convert the data to JSON format
    data = {
        'months': monthly_summary['Month'].tolist(),
        'total_sales_values': monthly_summary['Value of sale'].tolist()
    }

    return jsonify(data)

@app.route('/advisor_summary_data')
def advisor_summary_data():
    # Calculate the total sales value for each advisor for each month
    advisor_summary = df.groupby(['Advisor Name', 'Month'])['Value of sale'].sum().reset_index()

    # Convert the data to JSON format
    data = {
        'months': advisor_summary['Month'].unique().tolist(),
        'advisors': []
    }

    for advisor in advisor_summary['Advisor Name'].unique():
        advisor_data = advisor_summary[advisor_summary['Advisor Name'] == advisor]
        data['advisors'].append({
            'name': advisor,
            'total_sales_values': advisor_data['Value of sale'].tolist()
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
