import requests
import json
import pandas as pd
from datetime import datetime
from BiliBili import BiliBili
import cookieM

bw_park = BiliBili(cookieM.load_cookie())
bws_info = bw_park.bws_info()

processed_data = []


# 获取所有预约数据
for screen_date_str, reserves in bws_info['reserve_list'].items():
    for item in reserves:
        # 解析预约时间
        reserve_begin_timestamp = item["reserve_begin_time"]
        reserve_time = datetime.fromtimestamp(reserve_begin_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # 解析活动日期
        screen_date = int(screen_date_str)
        year = screen_date // 10000
        month = (screen_date // 100) % 100
        day = screen_date % 100
        activity_date = f"{year}-{month:02d}-{day:02d}"

        # 活动名称和活动代码
        act_title = item["act_title"]
        activity_code = item["reserve_id"]  # 默认使用 reserve_id 作为活动代码

        processed_data.append({
            "预约时间": reserve_time,
            "活动日期": activity_date,
            "活动名称": act_title,
            "活动代码": activity_code
        })

# 创建 DataFrame 并保存为 CSV
df = pd.DataFrame(processed_data)
df.to_csv("processed_data_from_json.csv", index=False, encoding="utf-8-sig")

print("表格已成功生成并保存为 processed_data_from_json.csv")