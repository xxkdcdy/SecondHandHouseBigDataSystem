from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

dict_region = {}

p = Options()
p.add_argument('--whitelisted-ips')
p.add_argument('--no-sandbox')
p.add_argument('--disable-extensions')
browser = webdriver.Chrome(options=p)
browser.maximize_window()
url = 'https://bj.lianjia.com/ershoufang/dongcheng/'   # url需要是点击其中一个区域后的url，让网站把position挂载出来
browser.get(url=url)
time.sleep(6)
div_region = browser.find_elements_by_xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a')
for i in range(len(div_region)):
    region = browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a[{}]'.format(i + 1))
    region_text = region.text
    dict_region[region_text] = []
    region.click()
    for position in browser.find_elements_by_xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a'):
        print(position.text)
        dict_region[region_text].append(position.text)

max_length = 0
print(dict_region.keys())
for key in dict_region.keys():
    print(dict_region[key], len(dict_region[key]))
    max_length = max(max_length, len(dict_region[key]))
for key in dict_region.keys():
    while len(dict_region[key]) < max_length:
        dict_region[key].append("")
df = pd.DataFrame(dict_region)
df.to_excel(r'F:/PyCharm/scsx/static/地区数据.xls')
browser.close()
