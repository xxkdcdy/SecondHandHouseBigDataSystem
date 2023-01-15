from flask_admin import BaseView, expose
import sqlite3
import Constraint as constraint
from flask import request
import math

'''
作者：cdy
组件：数据显示界面
'''


class Data(BaseView):
    @expose('/', methods=["GET"])
    def index(self):
        if request.method == "GET":
            p = request.args.get("page")  # p是页码
        if p is None:
            p = '1'
        elif int(p) < 1:
            p = '1'
        # 计算出最大页数max_page
        max_page = math.ceil(len(constraint.select_all()) / constraint.page_size)
        if int(p) > max_page:
            p = str(max_page)
        k = (int(p) - 1) * constraint.page_size
        con = sqlite3.connect(constraint.path)
        cur = con.cursor()
        # 只取出当前页码所对应的数据显示
        cur.execute("select * from shHouse limit {}, {}".format(k, constraint.page_size))
        msgs = cur.fetchall()
        cur.close()
        con.close()
        # 第一个变量是显示的Html文件，后面的参数传到Html中
        return self.render('data.html', msgs=msgs, page=p, max_page=max_page)
