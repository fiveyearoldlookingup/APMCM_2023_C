import pandas as pd

def aggregate_monthly_production(file_path, output_file_path):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Check if '数据日期' column is datetime type, if not convert it
    if not pd.api.types.is_datetime64_any_dtype(data['Date']):
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Extract year and month from the '数据日期' column
    data['Year'] = data['Sales volume'].dt.year
    data['Month'] = data['Sales volume'].dt.month

    # Filtering out the row with headers in data values
    data_filtered = data[data['Sales volume'] ]

    # Converting '产量' to numeric for sum operationc
    data_filtered['Sales volume）'] = pd.to_numeric(data_filtered['Sales volume'], errors='coerce')

    # Grouping by year and month and calculating the sum of production for each group
    #grouped_data = data_filtered.groupby(['Year', 'Month'])['涉案金额（元）'].sum().reset_index()
    grouped_data = data_filtered.groupby(['Year'])['Sales volume'].sum().reset_index()

    # Save the result to an Excel file
    grouped_data.to_excel(output_file_path, index=False)

# Replace 'your_file_path_here' with the actual path of your Excel file

file_path = 'C:/Users/35274/Desktop/亚太杯/副本1.Data.xlsx'#C:\Users\35274\Desktop\亚太杯\副本1.Data.xlsx"
output_file_path = '111yearly_production_sum.xlsx' # You can change the file name and path as needed

aggregate_monthly_production(file_path, output_file_path)#""C:\Users\35274\Desktop\31汽车上市公司诉讼仲裁数据(200308-202303).xlsx""
print(f"Data has been saved to {output_file_path}")
