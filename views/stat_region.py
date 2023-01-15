from flask_admin import BaseView, expose
import matplotlib
import matplotlib.pyplot as plt
import base64
import io
import Constraint as constraint
matplotlib.use('Agg')  # "main thread is not in main loop" Error 的处理方式

'''
作者：cdy
组件：按区域分布界面
'''


class StatRegion(BaseView):
    @expose('/')
    def index(self):
        img = io.BytesIO()
        data = constraint.std_data()
        plt.figure(figsize=(14, 8))
        plt.title("镇江二手房按房屋区域分布饼状图")
        data['位置1'].value_counts().plot.pie(autopct='%.2f%%')
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return self.render('stat.html', plot_url=plot_url)
