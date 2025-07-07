# 提示用户输入多行文本（输入空行表示结束）
print("请输入原始 Cookie 文本内容（每行一个 key: value，输入空行结束）：")
lines = []
while True:
    try:
        line = input()
        if not line.strip():  # 如果输入的是空行，结束输入
            break
        lines.append(line)
    except EOFError:
        break

raw_text = "\n".join(lines)

# 处理每一行
result = []
for line in raw_text.strip().split('\n'):
    if ':' in line:
        key, value = line.split(':', 1)  # 只分割一次
        result.append(f"{key.strip()}={value.strip()}")

# 拼接最终 Cookie 字符串
cookie_str = "; ".join(result)

# 保存到 cookie.txt 文件
with open("cookie.txt", "w", encoding="utf-8") as f:
    f.write(cookie_str)

print("转换完成，结果已保存至 cookie.txt 文件。")