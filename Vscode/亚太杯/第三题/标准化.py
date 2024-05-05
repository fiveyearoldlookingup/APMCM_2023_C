import pandas as pd
from sklearn.preprocessing import StandardScaler

# 加载Excel文件
file_path = 'E:/科研程序/代码/vscode/亚太杯/亚太杯/第三题/DATA新.xlsx'  # 替换为您的文件路径"E:\科研程序\代码\vscode\亚太杯\亚太杯\第三题\DATA新.xlsx"

# 加载第一张工作表
df_sheet1 = pd.read_excel(file_path, sheet_name=0)

# 需要标准化的列
columns_to_standardize = ['ZH Sales volume', 'Market Share', 'Global traditional energy vehicle sales', 'Global Pure electric sales', 'Plug-in sales']

# 使用StandardScaler进行标准化
scaler = StandardScaler()
df_sheet1_standardized = df_sheet1.copy()
df_sheet1_standardized[columns_to_standardize] = scaler.fit_transform(df_sheet1[columns_to_standardize])

# 将标准化后的数据保存到新的工作表中
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:  
    df_sheet1_standardized.to_excel(writer, sheet_name='Sheet3', index=False)
