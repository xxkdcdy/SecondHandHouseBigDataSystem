from flask import Flask
from flask_admin import Admin, AdminIndexView
import views.data as dataview
import views.stat_region as region
import views.stat_price as price
import views.stat_unitprice as unit_price
import views.stat_price_displot as price_dis
import views.predict as predict

'''
作者：cdy
组件：可视化运行界面，直接运行就可以启动Web端
'''


# 初始化flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# 初始化flask-admin
admin = Admin(
    app,
    name='镇江市二手房大数据平台',
    index_view=AdminIndexView(
        name='导航栏',
        template='welcome.html',
        url='/'
    )
)

# 在flask-admin中注册路由，并将组件名加载到导航栏上
admin.add_view(dataview.Data(name='数据'))
admin.add_view(region.StatRegion(name='按区域', category='统计'))
admin.add_view(price.StatPrice(name='按价格', category='统计'))
admin.add_view(unit_price.StatUnitPrice(name='按小区', category='统计'))
admin.add_view(price_dis.StatPriceDis(name='直方图', category='统计'))
admin.add_view(predict.StatPredict(name='预测'))
app.run()   # 运行flask
