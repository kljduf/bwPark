import json
from datetime import datetime, timedelta
# 用户输入 cookie 字符串
cookie_str = input("请输入完整的 Cookie 字符串：").strip()

# 需要保留的字段
target_keys = {
    "SESSDATA", "bili_jct", "DedeUserID", "DedeUserID__ckMd5",
    "sid", "Buvid", "timeMachine", "_uuid", "buvid3", "b_nut", "buvid4"
}

# 默认属性
default_attrs = {
    "domain": ".bilibili.com",
    "hostOnly": False,
    "httpOnly": False,
    "path": "/",
    "sameSite": None,
    "secure": False,
    "storeId": None,
    "session": False,
    "value": "",
}

# 解析 cookie
result = []

for item in cookie_str.split(";"):
    if "=" not in item:
        continue
    key, value = item.strip().split("=", 1)
    if key not in target_keys:
        continue

    cookie = default_attrs.copy()
    cookie["name"] = key
    cookie["value"] = value
    cookie["expirationDate"] = (datetime.now() + timedelta(days=365)).timestamp()
    # # 判断是否包含 expirationDate（比如 SESSDATA 的值中可能包含过期时间）
    # if key == "SESSDATA":
    #     try:
    #         parts = value.split(",")
    #         if len(parts) >= 2:
    #             exp_time = int(parts[1])
    #             cookie["expirationDate"] = exp_time
    #             cookie["session"] = False
    #         else:
    #             cookie["session"] = True
    #     except Exception:
    #         cookie["session"] = True
    # elif key in ["bili_jct", "DedeUserID", "DedeUserID__ckMd5"]:
    #     # 这些字段通常与登录有关，设置 session=False 并使用默认 expirationDate（可选）
    #     cookie["session"] = False
    #     cookie["expirationDate"] = 1767157610  # 示例值，可根据需要修改
    # else:
    #     # 其他字段默认是 session cookie
    #     cookie["session"] = True

    result.append(cookie)

# 写入文件
with open("cookie.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("处理完成，结果已保存至 cookie.json")