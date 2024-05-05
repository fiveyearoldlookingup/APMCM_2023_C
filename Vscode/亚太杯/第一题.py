import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import seaborn as sns  # 导入seaborn库进行美化

# 设置Seaborn的样式
sns.set(style="whitegrid")

# 加载数据
data = pd.read_excel('E:/科研程序/代码/vscode/亚太杯/亚太杯/第一题/DATA新.xlsx')

# 数据预处理
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 提取关键列
sales_volume = data['Sales volume']
infrastructure = data['Number of public charging piles_Nationwide (cumulative)']

# 构建和拟合ARIMA模型
model_sales = SARIMAX(sales_volume, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12))
results_sales = model_sales.fit()

model_infra = SARIMAX(infrastructure, order=(0, 2, 0), seasonal_order=(1, 1, 0, 12))
results_infra = model_infra.fit()

# 合并数据用于交叉相关和Granger因果检验
combined_data = pd.concat([sales_volume, infrastructure], axis=1)

# 时间序列图
plt.figure(figsize=(14, 7))
plt.plot(sales_volume, color='blue', label='Sales Volume')
plt.plot(infrastructure, color='green', label='Infrastructure')
plt.title('Sales Volume and Infrastructure Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()

# 交叉相关分析
fig, ax = plt.subplots(1, 2, figsize=(16, 5))
plot_acf(combined_data['Sales volume'], ax=ax[0], lags=30)
ax[0].set_title('Autocorrelation of Sales Volume')
ax[0].set_xlabel('Lag')
ax[0].set_ylabel('ACF')

plot_pacf(combined_data['Sales volume'], ax=ax[1], lags=30)
ax[1].set_title('Partial Autocorrelation of Sales Volume')
ax[1].set_xlabel('Lag')
ax[1].set_ylabel('PACF')
plt.tight_layout()
plt.show()

# Granger因果检验的P值条形图
p_values = {lag: min(test[1] for test in result[0].values()) for lag, result in grangercausalitytests(combined_data, maxlag=12, verbose=False).items()}
plt.figure(figsize=(10, 5))
sns.barplot(x=list(p_values.keys()), y=list(p_values.values()), palette='muted')
plt.axhline(0.05, ls='--', color='red')  # 显著性水平线
plt.title('Granger Causality Test P-Values')
plt.xlabel('Lags')
plt.ylabel('P-Value')
plt.show()



# Granger因果检验
max_lag = 12
test_result = grangercausalitytests(combined_data, max_lag, verbose=True)

# 提取Granger因果检验的p值
p_values = [test_result[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag+1)]

# 创建p值热图
plt.figure(figsize=(10, 6))
sns.heatmap([p_values], annot=True, xticklabels=list(range(1, max_lag+1)), yticklabels=['P Value'], cmap='coolwarm', cbar=True)
plt.title('Granger Causality Test P-Values')#格兰杰因果检验 P 值热图
plt.xlabel('Lags')
plt.tight_layout()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为 SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.show()
