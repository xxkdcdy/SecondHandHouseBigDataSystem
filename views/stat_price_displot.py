from flask_admin import BaseView, expose
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import Constraint as constraint
matplotlib.use('Agg')  # "main thread is not in main loop" Error 的处理方式

'''
作者：cdy
组件：直方图界面
'''


class StatPriceDis(BaseView):
    @expose('/')
    def index(self):
        img = io.BytesIO()
        data = constraint.std_data()
        plt.figure(figsize=(14, 8))
        plt.subplot(1, 2, 1)
        plt.title("均价直方图")
        sns.distplot(data['均价'])
        data['均价'].mean()
        plt.subplot(1, 2, 2)
        plt.title("总价直方图")
        sns.distplot(data['总价'])
        data['总价'].mean()
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return self.render('stat.html', plot_url=plot_url)
