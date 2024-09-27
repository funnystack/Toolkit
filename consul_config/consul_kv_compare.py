import requests
import time
import threading
from collections import defaultdict
import consul_kv_backup

# Consul集群的地址
consul_a_url = 'http://adconsul.funny.com'
consul_b_url = 'http://lfconsul.funny.com'
ui_path = "/ui/dc1/kv/"
a_keys = None
b_keys = None


# 遍历key的函数
def list_keys(url):
    response = requests.get(f"{url}/v1/kv/?keys")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error listing keys: {response.status_code}")
        return []


# 获取key的value的函数
def get_key_value(url, key):
    response = requests.get(f"{url}/v1/kv/{key}")
    if response.status_code == 200:
        value = response.json()[0]['Value']
        return value
    else:
        print(f"Error getting key value: {response.status_code}")
        return None


# 比较key数量的函数
def compare_key_count():
    while True:
        print('compare_key_count start!')
        a_keys = list_keys(consul_a_url)
        b_keys = list_keys(consul_b_url)
        missing_in_a = set(b_keys) - set(a_keys)
        missing_in_b = set(a_keys) - set(b_keys)
        if missing_in_a:
            consul_kv_backup.send_ding_alarm(f"亦庄consul集群缺少key: {', '.join(missing_in_a)}")
        if missing_in_b:
            consul_kv_backup.send_ding_alarm(f"华为云consul集群缺少key: {', '.join(missing_in_b)}")
        time.sleep(300)  # 每5分钟检查一次


# 比较key的value的函数
def compare_key_values():
    count = 0
    alertMsg = ''
    print('compare_key_values start!')
    for key in a_keys:
        if key in b_keys:
            a_value = get_key_value(consul_a_url, key)
            b_value = get_key_value(consul_b_url, key)
            if a_value != b_value and a_value is not None and b_value is not None:
                count = count + 1
                alertMsg = alertMsg + f"\\n\\nvalue不一致的key:{key} \\n亦庄consul集群地址:{consul_a_url + ui_path + key}/edit \\n华为云consul集群地址:{consul_b_url + ui_path + key}/edit"
    title = 'value不一致的key共' + str(count) + '个,明细如下:'
    print(title + alertMsg)
    consul_kv_backup.send_ding_alarm(title + alertMsg)


# 订阅key变更的函数
def subscribe_key_changes(url, group, last_values, last_keys):
    print('subscribe_key_changes start:' + url)
    while True:
        current_keys = set(list_keys(url))
        new_keys = current_keys - last_keys
        removed_keys = last_keys - current_keys
        for key in new_keys:
            consul_kv_backup.send_ding_alarm(f"{group}consul集群新增key:{key} \\n地址:{url + ui_path + key}/edit")
        for key in removed_keys:
            consul_kv_backup.send_ding_alarm(f"{group}consul集群的key:{key}被删除")
        last_keys = current_keys

        start_time = time.time()  # 开始时间
        for key in current_keys:
            current_value = get_key_value(url, key)
            if key in last_values:
                if current_value != last_values[key]:
                    consul_kv_backup.send_ding_alarm(
                        f"{group}consul集群的key:{key}发生了变更 \\n地址: {url + ui_path + key}/edit")
            last_values[key] = current_value
        end_time = time.time()  # 结束时间
        elapsed_time = end_time - start_time  # 计算经过的时间
        print(f"代码执行时间：{elapsed_time}秒")
        time.sleep(300)  # 每5分钟检查一次


# 主函数
def main():
    # 比较key的数量
    # compare_key_count_thread = threading.Thread(target=compare_key_count)
    # compare_key_count_thread.start()

    # 比较key的value
    # compare_key_values_thread = threading.Thread(target=compare_key_values)
    # compare_key_values_thread.start()

    # 订阅key变更
    a_last_values = defaultdict(str)
    b_last_values = defaultdict(str)
    a_last_keys = set(a_keys)
    b_last_keys = set(b_keys)
    threading.Thread(target=subscribe_key_changes, args=(consul_a_url, 'A', a_last_values, a_last_keys)).start()
    threading.Thread(target=subscribe_key_changes, args=(consul_b_url, 'B', b_last_values, b_last_keys)).start()


if __name__ == "__main__":
    # 获取A集群和B集群的key
    a_keys = list_keys(consul_a_url)
    b_keys = list_keys(consul_b_url)
    main()
