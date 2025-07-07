import ntplib
config = {}
c = ntplib.NTPClient()
skip = False
try:
    response = c.request('ntp.tencent.com')
except Exception:
    print("时间同步出现错误，将跳过时间检查")
    skip = True
if skip == False:
    time_offset = response.offset
    if time_offset > 0.5:
        print(f"当前时间偏移：{time_offset:.2f}秒，建议校准时间")
    config["time_offset"] = time_offset
else:
    config["time_offset"] = 0

print(config["time_offset"] )