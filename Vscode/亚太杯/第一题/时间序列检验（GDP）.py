import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_excel('E:/科研程序/代码/vscode/亚太杯/亚太杯/第一题/DATA新.xlsx')

# 数据预处理
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 提取关键列
sales_volume = data['Sales volume']
infrastructure = data['Amount involved (yuan)']

# 函数：检查平稳性并进行差分
def make_stationary(series):
    adf_test = adfuller(series.dropna())
    print(f'ADF Statistic: {adf_test[0]}')
    print(f'p-value: {adf_test[1]}')

    if adf_test[1] > 0.05:
        # 尝试一阶差分
        series_diff = series.diff().dropna()
        adf_test_diff = adfuller(series_diff)
        print(f'ADF Statistic (1st diff): {adf_test_diff[0]}')
        print(f'p-value (1st diff): {adf_test_diff[1]}')

        if adf_test_diff[1] > 0.05:
            # 尝试二阶差分
            series_diff = series_diff.diff().dropna()
            adf_test_diff = adfuller(series_diff)
            print(f'ADF Statistic (2nd diff): {adf_test_diff[0]}')
            print(f'p-value (2nd diff): {adf_test_diff[1]}')
            return series_diff
        else:
            return series_diff
    else:
        return series

# 检查平稳性并进行必要的差分
sales_volume_stationary = make_stationary(sales_volume)
infrastructure_stationary = make_stationary(infrastructure)

# 再次组合数据用于Granger因果检验
combined_data_stationary = pd.concat([sales_volume_stationary, infrastructure_stationary], axis=1).dropna()


# 将平稳化后的数据导出到Excel
combined_data_stationary.to_excel('E:/科研程序/代码/vscode/亚太杯/亚太杯/第一题/TimeStationaryData.xlsx')


# 进行Granger因果检验
granger_test_result = grangercausalitytests(combined_data_stationary, maxlag=12, verbose=False)

# 提取Granger因果检验的P值
p_values = {lag: min(test[1] for test in result[0].values()) for lag, result in granger_test_result.items()}

# 绘制P值条形图
plt.figure(figsize=(8, 4))
plt.bar(p_values.keys(), p_values.values(), color='skyblue')
plt.xlabel('Lags')
plt.ylabel('P-Value')
plt.title('Granger Causality Test Results (P-Values)')
plt.axhline(y=0.05, color='red', linestyle='--')  # 显著性水平线
plt.show()
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 进行Granger因果检验并获取P值
maxlag = 12
test_results = grangercausalitytests(combined_data_stationary, maxlag=maxlag, verbose=False)

# 提取特定检验（例如 ssr_ftest）的P值
p_values = np.zeros(maxlag)
for i in range(maxlag):
    p_values[i] = test_results[i+1][0]['ssr_ftest'][1]  # 这里使用了 ssr基于F检验的p值
    

# 绘制热力图
plt.figure(figsize=(10, 5))
sns.heatmap([p_values], annot=True, cmap='coolwarm', cbar_kws={'label': 'P-Value'})
plt.title('Granger Causality Test P-Values (ssr_ftest)')
plt.xlabel('Lag')
plt.xticks(np.arange(0.5, maxlag + 0.5), np.arange(1, maxlag + 1))
plt.yticks([])
plt.show()
print(p_values)