import pandas as pd
import os

path = r'D:\\Desktop\\data\\'


def work(file_name):
    df = pd.read_excel(path + r"file\\" + file_name)
    for i in df.columns:
        col = df[i]  # 提取单列数据
        print('*******------' * 20)
        print(col.max(), col.min())
        df[i] = col.apply(lambda x: ((x - col.min()) / (col.max() - col.min())))

    writer = pd.ExcelWriter(path + r"process\\" + file_name.replace(".xls", "new.xls"))
    df.to_excel(writer, index=False)
    writer.save()
    writer.close()


for file in os.listdir(path + r"file\\"):
    work(file)
