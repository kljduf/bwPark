import os

COOKIE_FILE = 'cookie.txt'

def trans(cookie_str):
    try:
        return {k: v for k, v in (cookie.split('=') for cookie in cookie_str.split('; '))}
    except:
        print("好像出问题了喵~\n")
        return prompt_manual_input()

def load_cookie():
    """尝试加载 Cookie，失败则提示用户输入"""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookie_str = f.read().strip()
            if cookie_str:
                print("Loading Cookie 喵~")
                return trans(cookie_str)

    # 如果文件不存在或内容为空，则提示用户输入
    return prompt_manual_input()


def prompt_manual_input():
    while True:
        cookie = input("请输入你的 B 站 Cookies 喵~\n").strip()
        if not cookie:
            print("不能留空喵~")
            continue
        # 保存为纯文本文件
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            f.write(cookie)
        return trans(cookie)


# 示例用法（运行该脚本时触发流程）
if __name__ == '__main__':
    cookie = load_cookie()
    print("最终使用的 Cookie 内容为：", cookie)