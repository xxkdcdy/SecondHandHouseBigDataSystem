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
组件：价格分布界面
'''


class StatPrice(BaseView):
    @expose('/')
    def index(self):
        img = io.BytesIO()
        data = constraint.std_data()
        plt.figure(figsize=(14, 8))
        plt.title("镇江二手房按房屋区域价格分布箱线图")
        sns.boxplot(data=data, x='位置1', y='均价')
        plt.savefig(img, format='png')
        img.seek(0)

        # 将图片转成BASE64格式，将这个字符串复制在Html界面上，就可以在浏览器中显示图片，其他可视化组件类似
        plot_url = base64.b64encode(img.getvalue()).decode()

        return self.render('stat.html', plot_url=plot_url)
