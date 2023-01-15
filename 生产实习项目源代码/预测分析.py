import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

'''
作者：cdy
组件：预测界面
'''


data = pd.read_excel(r'F:/PyCharm/scsx/static/链家二手房合并多页数据.xls')
labels = ['朝向', '建筑类型', '装修', '楼层']
data = data[data['城市'] == '柳州']
x = data[labels].copy()
y = data['房屋总价（万元）']
for col in labels:
    le = LabelEncoder()
    x[col] = le.fit_transform(x[col])
# 划分出6：2：2的训练集，侧式集和验证集
x_train, x_tmp, y_train, y_tmp = train_test_split(x, y, test_size=0.4)
x_test, x_val, y_test, y_val = train_test_split(x_tmp, y_tmp, test_size=0.5)
rf = RandomForestRegressor(n_estimators=2000, n_jobs=-1)

rf.fit(x_train, y_train)
rf_res = rf.predict(x_test)
fi = pd.DataFrame(
            {'x': x_train.columns, 'feature_importance': rf.feature_importances_})
fi = fi.sort_values(by='feature_importance', ascending=False)

print('预测均值', round(np.mean(rf_res), 2))
print('绝对值误差', round(mean_absolute_error(rf_res, y_test), 2))
print('特征重要性', fi)   # x='feature_importance', y='x'
