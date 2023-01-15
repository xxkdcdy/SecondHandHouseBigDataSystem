import matplotlib.pyplot as plt
import Constraint as constraint

'''
作者：cdy
组件：views包的入口，主要是matplotlib的显示设置
'''


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.size'] = constraint.font_size  # 设置字体大小
