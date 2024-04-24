from flask import Flask, jsonify

app = Flask(__name__)

# Sample monthly summary data
monthly_summary_data = {
    'months': ['October', 'November', 'December', 'January'],
    'total_sales_values': [10000, 15000, 12000, 18000],
    'number_of_calls': [50, 70, 60, 80],
    'average_values': [200, 214.28, 200, 225],
    'median_values': [190, 215, 210, 230]
}

# Sample advisor summary data
advisor_summary_data = {
    'months': ['October', 'November', 'December', 'January'],
    'advisors': [
        {
            'name': 'Advisor 1',
            'color': 'rgba(255, 99, 132, 1)',
            'total_sales_values': [5000, 6000, 5500, 7000]
        },
        {
            'name': 'Advisor 2',
            'color': 'rgba(54, 162, 235, 1)',
            'total_sales_values': [4000, 5500, 5000, 6500]
        }
    ]
}

@app.route('/monthly_summary_data')
def get_monthly_summary_data():
    return jsonify(monthly_summary_data)

@app.route('/advisor_summary_data')
def get_advisor_summary_data():
    return jsonify(advisor_summary_data)

if __name__ == '__main__':
    app.run(debug=True)
