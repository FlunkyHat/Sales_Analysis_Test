from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv('sales_data.csv')
df['Call Date'] = pd.to_datetime(df['Call Date'])
df['Month'] = df['Call Date'].dt.month_name()
df['Value of sale'] = pd.to_numeric(df['Value of sale'], errors='coerce')
df = df.dropna(subset=['Value of sale'])

# Calculate metrics
summary = df.groupby(['Advisor Name', 'Month'])['Value of sale'].agg(['count', 'sum', 'mean', 'median', 'min', 'max']).reset_index()
monthly_summary = df.groupby(['Month'])['Value of sale'].agg(['count', 'sum', 'mean', 'median', 'min', 'max']).reset_index()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    return "Test successful!"

@app.route('/monthly_summary')
def monthly_summary_route():
    fig = px.bar(monthly_summary, x='Month', y=['sum', 'count', 'mean', 'median', 'min', 'max'], title='Monthly Sales Summary',
                 labels={'sum': 'Total Sales Value', 'count': 'Number of Calls', 'mean': 'Average Value', 'median': 'Median Value', 'min': 'Minimum Value', 'max': 'Maximum Value'})
    fig.update_traces(hovertemplate='<br>'.join([
        'Month: %{x}',
        'Total Sales Value: %{y[0]:,.2f}',
        'Number of Calls: %{y[1]}',
        'Average Value: %{y[2]:,.2f}',
        'Median Value: %{y[3]:,.2f}',
        'Minimum Value: %{y[4]:,.2f}',
        'Maximum Value: %{y[5]:,.2f}'
    ]))
    return pio.to_html(fig)

@app.route('/advisor_summary/<advisor>')
def advisor_summary(advisor):
    advisor_data = summary[summary['Advisor Name'] == advisor]
    fig = px.bar(advisor_data, x='Month', y=['sum', 'count', 'mean', 'median', 'min', 'max'], title=f'Sales Summary for {advisor}',
                 labels={'sum': 'Total Sales Value', 'count': 'Number of Calls', 'mean': 'Average Value', 'median': 'Median Value', 'min': 'Minimum Value', 'max': 'Maximum Value'})
    fig.update_traces(hovertemplate='<br>'.join([
        'Month: %{x}',
        'Total Sales Value: %{y[0]:,.2f}',
        'Number of Calls: %{y[1]}',
        'Average Value: %{y[2]:,.2f}',
        'Median Value: %{y[3]:,.2f}',
        'Minimum Value: %{y[4]:,.2f}',
        'Maximum Value: %{y[5]:,.2f}'
    ]))
    return pio.to_html(fig)

@app.route('/monthly_summary_data')
def monthly_summary_data():
    # Convert the data to JSON format
    data = {
        'months': monthly_summary['Month'].tolist(),
        'total_sales_values': monthly_summary['sum'].tolist(),
        'number_of_calls': monthly_summary['count'].tolist(),
        'average_values': monthly_summary['mean'].tolist(),
        'median_values': monthly_summary['median'].tolist(),
        'min_values': monthly_summary['min'].tolist(),
        'max_values': monthly_summary['max'].tolist()
    }

    return jsonify(data)

@app.route('/advisor_summary_data')
def advisor_summary_data():
    # Convert the data to JSON format
    data = {
        'months': summary['Month'].unique().tolist(),
        'advisors': []
    }

    for advisor in summary['Advisor Name'].unique():
        advisor_data = summary[summary['Advisor Name'] == advisor]
        data['advisors'].append({
            'name': advisor,
            'total_sales_values': advisor_data['sum'].tolist(),
            'number_of_calls': advisor_data['count'].tolist(),
            'average_values': advisor_data['mean'].tolist(),
            'median_values': advisor_data['median'].tolist(),
            'min_values': advisor_data['min'].tolist(),
            'max_values': advisor_data['max'].tolist()
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
