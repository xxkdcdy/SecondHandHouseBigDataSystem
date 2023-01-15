import pandas as pd
import sys

paddings = {
    'liuzhou': '柳州',
    'sh': '上海',
    'sz': '深圳',
    'tj': '天津',
    'bj': '北京'
}
file_name = r'F:/PyCharm/scsx/static/链家二手房{}多页数据.xls'
df_all = pd.DataFrame()
headings_list = ['东', '南', '西', '北', '东北', '西北', '西南', '东南', '南北', '东西']
headings = pd.Series(headings_list)
floors = pd.DataFrame({
    '楼层1': ['地下室', '低层', '多层', '中高层', '高层', '超高层'],
    '楼层2': ['<1', '[1, 3]', '[4, 6]', '[7, 9]', '[10, 30]', '>30']
})
histories = pd.DataFrame({
    '3年内': ['>2020'],
    '10年内': ['[2013, 2019]'],
    '20年内': ['[2003, 2012]'],
    '30年内': ['[1993, 2002]'],
    '30年以上': ['<1993']
})


# 对房屋总价进行处理
def solve_price(x):
    x = x.replace("万", "")
    x = x.replace("参考价: ", "")
    return x


# 对房屋单价进行处理
def solve_u_price(x):
    x = x.replace("元/平", "")
    x = x.replace(",", "")
    return x


# 获取小区名称
def solve_post_village(x):
    split = x.split("-")
    if len(split) == 2:
        return split[0].strip(" \t\n")
    else:
        return "{}-{}".format(split[0], split[1]).strip(" \t\n")


# 获取板块
def solve_post_plate(x):
    split = x.split("-")
    if len(split) == 2:
        return split[1].strip(" \t\n")
    else:
        return split[2].strip(" \t\n")


# 获取厅室信息
def solve_house_hall(x):
    split = x.split("|")
    if '车位' in split[0].strip(" \t\n"):
        return '车位'
    return split[0].strip(" \t\n").split("室")[0] + "室"


def solve_house_hall_2(x):
    split = x.split("|")
    if '车位' in split[0].strip(" \t\n"):
        return '车位'
    return split[0].strip(" \t\n").split("室")[1]


# 获取面积信息
def solve_house_area(x):
    split = x.split("|")
    area = split[1].strip(" \t\n").replace("平米", "")
    return area


# 获取面积分组信息
def solve_house_area_group(x):
    if x <= 30:
        return "微房"
    elif x <= 60:
        return "小型"
    elif x <= 90:
        return "中型"
    elif x <= 150:
        return "大型"
    else:
        return "超大型"


# 获取朝向信息
def solve_house_heading(x):
    split = x.split("|")
    heading = split[2].strip(" \t\n")
    if heading in headings_list:
        return heading
    elif '南' in heading and '北' in heading:
        return '南北'
    elif '东' in heading and '北' in heading:
        return '东北'
    elif '西' in heading and '北' in heading:
        return '西北'
    elif '南' in heading and '东' in heading:
        return '东南'
    elif '南' in heading and '西' in heading:
        return '西南'
    else:
        return '东西'


# 获取装修信息
def solve_house_renovation(x):
    split = x.split("|")
    renovation = split[3].strip(" \t\n")
    return renovation


# 获取楼层信息
def solve_house_floor(x):
    split = x.split("|")
    if len(split) < 5:
        return "暂无数据"
    floor = split[4].strip(" \t\n")
    num = ''.join([x for x in floor if x.isdigit()])   # 提取字符串中的数字
    if len(num) == 0:
        return floor
    elif eval(num) < 1:
        return '地下室'
    elif 1 <= eval(num) <= 3:
        return '低层'
    elif 4 <= eval(num) <= 6:
        return '多层'
    elif 7 <= eval(num) <= 9:
        return '中高层'
    elif 10 <= eval(num) <= 30:
        return '高层'
    else:
        return '超高层'


# 获取建筑时间信息
def solve_house_history(x):
    split = x.split("|")
    if len(split) < 6:
        return "暂无数据"
    history = split[5].strip(" \t\n")
    num = ''.join([x for x in history if x.isdigit()])  # 提取字符串中的数字
    if len(num) == 0:
        return "暂无数据"
    elif 2020 <= eval(num) <= 2023:
        return "3年内"
    elif 2013 <= eval(num) <= 2019:
        return "10年内"
    elif 2003 <= eval(num) <= 2012:
        return "20年内"
    elif 1993 <= eval(num) <= 2002:
        return "30年内"
    else:
        return "30年以上"


# 获取类型信息
def solve_house_type(x):
    split = x.split("|")
    if len(split) < 6:
        return "暂无数据"
    _type = split[5].strip(" \t\n")
    num = ''.join([x for x in _type if x.isdigit()])  # 提取字符串中的数字
    if len(num) > 0 and len(split) >= 7:
        _type = split[6].strip(" \t\n")
    return _type


for city in paddings.keys():
    df = pd.read_excel(file_name.format(city))
    # 根据行数增加一列“城市”
    df['城市'] = [paddings[city]] * df.shape[0]
    # 将当前城市的结果合并到合并表中
    df_all = pd.concat([df_all, df], axis=0)


# 对房屋区域进行处理
df_all['小区名称'] = df_all['房屋区域'].apply(solve_post_village)
df_all['板块'] = df_all['房屋区域'].apply(solve_post_plate)
df_all = df_all.drop(["房屋区域"], axis=1)

# 对房屋信息进行处理
df_all['室'] = df_all['房屋信息'].apply(solve_house_hall)
df_all['厅'] = df_all['房屋信息'].apply(solve_house_hall_2)
df_all['面积'] = df_all['房屋信息'].apply(solve_house_area).astype(float)
df_all['面积分组'] = df_all['面积'].apply(solve_house_area_group)
df_all['朝向'] = df_all['房屋信息'].apply(solve_house_heading)
df_all['装修'] = df_all['房屋信息'].apply(solve_house_renovation)
df_all['楼层'] = df_all['房屋信息'].apply(solve_house_floor)
df_all['建筑时间'] = df_all['房屋信息'].apply(solve_house_history)
df_all['建筑类型'] = df_all['房屋信息'].apply(solve_house_type)
df_all = df_all.drop(["房屋信息"], axis=1)

# 对房屋总价和单价进行处理
df_all['房屋总价'] = df_all['房屋总价'].apply(solve_price).astype(float)
df_all['房屋单价'] = df_all['房屋单价'].apply(solve_u_price).astype(float)

# 重置索引，保存到Excel表格
df_all = df_all.fillna(value="暂无数据")
df_all = df_all.rename(columns={'房屋总价': '房屋总价（万元）'})  # 重命名列，保证一致性
print(df_all.head(3))
print(df_all.describe())
df_all = df_all.reset_index(drop=True)

writer = pd.ExcelWriter(file_name.format("合并"))
df_all.to_excel(writer, sheet_name='总数据表', index=False)
headings.to_excel(writer, sheet_name='朝向表', index=False, header=['朝向'])
floors.to_excel(writer, sheet_name='楼层', index=False)
writer.save()
writer.close()

print(sys.version_info)
