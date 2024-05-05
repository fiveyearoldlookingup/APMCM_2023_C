import pandas as pd

def aggregate_lawsuit_amounts(file_path, output_file_path):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Ensure '公告日期' is datetime type
    data['公告日期'] = pd.to_datetime(data['公告日期'], errors='coerce')

    # Extract year and month from the '公告日期' column
    data['Year'] = data['公告日期'].dt.year
    data['Month'] = data['公告日期'].dt.month

    # Converting '涉案金额（元）' to numeric for sum operation
    data['涉案金额（元）'] = pd.to_numeric(data['涉案金额（元）'], errors='coerce')

    # Grouping by year and month and calculating the sum of lawsuit amounts for each group
    grouped_data = data.groupby(['Year', 'Month'])['涉案金额（元）'].sum().reset_index()

    # Save the result to an Excel file
    grouped_data.to_excel(output_file_path, index=False)

# Replace 'your_file_path_here' with the actual path of your Excel file
file_path = 'C:/Users/35274/Desktop/31汽车上市公司诉讼仲裁数据(200308-202303).xlsx'
output_file_path = 'aggregated_lawsuit_data.xlsx' # You can change the file name and path as needed

aggregate_lawsuit_amounts(file_path, output_file_path)
print(f"Aggregated lawsuit data has been saved to {output_file_path}")
