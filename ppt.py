import os
import requests
import pandas as pd

# 指定文件路径和文件名
file_path = '/Users/fangli/Desktop/ppt_tools/ppt_tools.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 获取第一列的所有链接
links = df.iloc[:, 0]

# 添加http前缀
links = ['http:' + link for link in links]

# 下载所有文件
for link in links:
    response = requests.get(link)
    with open(os.path.join('/Users/fangli/Desktop/ppt_tools/', link.split('/')[-1]), 'wb') as f:
        f.write(response.content)
        print(link)
