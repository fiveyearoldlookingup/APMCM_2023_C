import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_excel('E:/科研程序/代码/vscode/亚太杯/1.Data(中文).xlsx')#"E:\科研程序\代码\vscode\亚太杯\Data.xlsx"

# 数据预处理：转换列为正确的数据类型
data['销售数量'] = pd.to_numeric(data['销售数量'], errors='coerce')
data['公共类充电桩数量_全国（累加）'] = pd.to_numeric(data['公共类充电桩数量_全国（累加）'], errors='coerce')
data['GDP（月）'] = pd.to_numeric(data['GDP（月）'], errors='coerce')
data['电池容量(km)'] = pd.to_numeric(data['电池容量(km)'], errors='coerce')
#data['最高时速(km/h)'] = pd.to_numeric(data['最高时速(km/h)'], errors='coerce')
print(data.dtypes)

# 处理缺失值
data.fillna(0, inplace=True)
# 创建月份和年份的虚拟变量
# 创建虚拟变量
#dummy_months = pd.get_dummies(data['月份'], prefix='月份', drop_first=True)
#dummy_years = pd.get_dummies(data['年份'], prefix='年份', drop_first=True)

# 合并虚拟变量到数据集
#data = pd.concat([data, dummy_months, dummy_years], axis=1)



# 选择因变量和自变量
y = data['销售数量']
X = data.iloc[:, 1:]  # 从第三列开始到最后一列，即所有的自变量


# 定义自变量和因变量
#X = data[['公共类充电桩数量_全国（累加）', 'GDP（月）', '电池容量(km)', '最高时速(km/h)'] + list(dummy_months.columns) + list(dummy_years.columns)]
#y = data['销售数量']

# 添加常数项（截距）
X = sm.add_constant(X)

# 构建并拟合多元线性回归模型
model = sm.OLS(y, X).fit()
summary = model.summary()
# 输出模型结果
print(summary)
# 将回归结果转换为表格
results_as_html = summary.tables[1].as_html()
results_df = pd.read_html(results_as_html, header=0, index_col=0)[0]

# 导出到Excel
results_df.to_excel('回归结果改.xlsx')

# 可视化实际值与预测值
predictions = model.predict(X)
plt.figure(figsize=(10, 5))
plt.plot(y, label='Actual Sales')
plt.plot(predictions, label='Predicted Sales', alpha=0.7)
plt.title('Actual vs Predicted Sales')
plt.xlabel('Index')
plt.ylabel('Sales Quantity')
plt.legend()
plt.show()


#####进行wald检验#####