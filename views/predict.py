from flask_admin import BaseView, expose
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor
import pandas as pd
import seaborn as sns
import Constraint as constraint

matplotlib.use('Agg')  # "main thread is not in main loop" Error 的处理方式

'''
作者：cdy
组件：预测界面
'''


class StatPredict(BaseView):
    data = constraint.std_data()
    x = data.drop(columns=['id', '总价', '均价', '小区名'])
    y = data['均价']
    for col in ['位置1', '物业费', '容积率', '绿化率']:
        le = LabelEncoder()
        x[col] = le.fit_transform(x[col])
    # 划分出6：2：2的训练集，侧式集和验证集
    x_train, x_tmp, y_train, y_tmp = train_test_split(x, y, test_size=0.4)
    x_test, x_val, y_test, y_val = train_test_split(x, y, test_size=0.5)
    dt = DecisionTreeRegressor()
    rf = RandomForestRegressor(n_estimators=2000, n_jobs=-1)
    cb = CatBoostRegressor()

    def generateData(self):
        self.dt.fit(self.x_train.drop(columns='小区均价'), self.y_train)
        self.rf.fit(self.x_train.drop(columns='小区均价'), self.y_train)
        self.cb.fit(self.x_train.drop(columns='小区均价'), self.y_train)
        dt_res = self.dt.predict(self.x_test.drop(columns='小区均价'))
        rf_res = self.rf.predict(self.x_test.drop(columns='小区均价'))
        cb_res = self.cb.predict(self.x_test.drop(columns='小区均价'))
        predata = [
            ['预测均值',
             round(np.mean(dt_res), 2),
             round(np.mean(rf_res), 2),
             round(np.mean(cb_res), 2)],
            ['绝对值误差',
             round(mean_absolute_error(dt_res, self.y_test), 2),
             round(mean_absolute_error(rf_res, self.y_test), 2),
             round(mean_absolute_error(cb_res, self.y_test), 2)],
        ]
        return predata

    @expose('/')
    def index(self):
        img = io.BytesIO()

        msgs = self.generateData()
        plt.figure(figsize=(14, 6))
        plt.title("特征重要性")
        fi = pd.DataFrame(
            {'x': self.x_train.drop(columns='小区均价').columns, 'feature_importance': self.rf.feature_importances_})
        fi = fi.sort_values(by='feature_importance', ascending=False)
        sns.barplot(x='feature_importance', y='x', data=fi)
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return self.render('predict.html', plot_url=plot_url, msgs=msgs)
