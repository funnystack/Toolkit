import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 目标网页URL
url = 'https://gesp.ccf.org.cn/101/1010/10134.html'

# 发送HTTP请求
response = requests.get(url)
response.raise_for_status()  # 确保请求成功

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 寻找包含文件夹名称的div元素，这里假设每个class=indexNoticeDetails的div下只有一个子div且class=title
folder_divs = soup.find_all('div', class_='indexNoticeDetails')

# 确保至少找到一个文件夹名称
if not folder_divs:
    print("No folder name found on the page.")
else:
    # 遍历每个class=indexNoticeDetails的div元素
    for folder_div in folder_divs:
        # 提取文件夹名称，这里假设文件夹名称是div的子div且class=title的html文本
        folder_name = folder_div.find('div', class_='title').text.strip()

        # 确保文件夹名称不为空
        if folder_name:
            # 确保这个目录存在，如果不存在就创建它
            download_directory = os.path.join('downloaded_files', folder_name)
            if not os.path.exists(download_directory):
                os.makedirs(download_directory)

            # 寻找当前文件夹下的所有PDF链接
            pdf_links = folder_div.find_all('a', href=True, title=True)

            # 下载每个PDF文件
            for pdf_link in pdf_links:
                pdf_title = pdf_link['title'].strip()
                pdf_url = urljoin(url, pdf_link['href'])

                # 发送HTTP请求下载PDF
                pdf_response = requests.get(pdf_url, stream=True)
                pdf_response.raise_for_status()  # 确保请求成功

                # 为文件生成一个合适的文件名
                filename = os.path.join(download_directory, pdf_title) + '.pdf'

                # 写文件
                with open(filename, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f'Downloaded {pdf_title} to {download_directory}')

    print('All PDFs have been downloaded.')
