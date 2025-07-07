import requests
import time

def measure_http_latency(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        end = time.time()
        latency = (end - start) * 1000  # 转换为毫秒
        print(f"HTTP 请求 {url} 成功\n延迟为：{latency:.2f} 毫秒")
        return latency
    except requests.RequestException as e:
        print(f"请求失败：{e}")
        return None

# 示例
measure_http_latency("https://api.bilibili.com/x/activity/bws/online/park/reserve/do")