import requests, base64, os, shutil, json

# repo的name 务必与git_url的名称一致
repo_name = 'consul_config'
base_path = '/app/repo/'
repo_path = base_path + repo_name
# 指定文件夹路径
folder_path = base_path + repo_name


# 1. 请求获取数据中心列表
def get_datacenters(consul_server):
    url = f'{consul_server}/v1/catalog/datacenters'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: Unable to get datacenters, status code: {response.status_code}')
        return None


# 2. 请求获取键值对
def get_keys(consul_server, dc):
    url = f'{consul_server}/v1/kv/?keys'
    params = {'dc': dc}
    print(url)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: Unable to get keys, status code: {response.status_code}')
        return None


# 3. 遍历请求键值对详细信息
def get_key_details(consul_server, dc, key):
    url = f'{consul_server}/v1/kv/{key}?dc={dc}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f'Error: Unable to get details for key {key}, status code: {response.status_code} ,content: {response.content}')


def write_key_backup(key, dc, consul_server, git_location):
    if not key.endswith('/'):
        print("处理key=" + key)
        key_detail = get_key_details(consul_server, dc, key)
        print(key_detail)
        key_value = key_detail[0].get('Value')
        if key_value is None or key_value == '':
            print('Value is None')
        else:
            decoded_string = base64.b64decode(key_detail[0]['Value'])
            # 截取最后一个 / 前的内容
            if '/' in key:
                real_path = folder_path + git_location + '/' + key.rsplit('/', 1)[0]
                # 指定文件名
                file_name = key.rsplit('/', 1)[1]
            else:
                real_path = folder_path + git_location
                # 指定文件名
                file_name = key
            # 构造完整的文件路径
            file_path = os.path.join(real_path, file_name)
            # 确保文件夹路径存在，如果不存在则创建
            if not os.path.exists(real_path):
                os.makedirs(real_path)
            # 打开文件进行写入
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(decoded_string.decode('utf-8'))


def consul_group_back(consul_server, git_location):
    # 获取数据中心
    datacenters = get_datacenters(consul_server)
    if datacenters:
        # 假设我们只关心第一个数据中心
        dc = datacenters[0]
        print(f'Datacenter: {dc}')

        # 获取所有键
        keys = get_keys(consul_server, dc)
        print(keys)
        if keys:
            for key in keys:
                write_key_backup(key, dc, consul_server, git_location)

def send_ding_alarm(msg):
    print(msg)

if __name__ == '__main__':
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    consul_group_back('http://test.consul.funny.com', '/key/test')
    consul_group_back('http://prod.consul.funny.com', '/key/prod')
