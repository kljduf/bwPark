import requests
class BiliBili:
    def __init__(self, cookies) -> None:
        self.cookies = cookies
        self.csrf_token = self.cookies['bili_jct']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/540.36 (KHTML, like Gecko)"}
        self.session = requests.Session()

    def bws_info(self):
        url = f"https://api.bilibili.com/x/activity/bws/online/park/reserve/info?csrf={self.csrf_token}&reserve_type=-1&reserve_date=20250711,20250712,20250713"
        res_info = self.session.get(url, headers=self.headers, cookies=self.cookies).json()

        if res_info['code'] != 0:
            print(f"cookies err: {res_info['code']} msg:{res_info['message']}")
            return False
        return res_info['data']

    def bws_do(self, ticket_no, inter_reserve_id):
        url = f"https://api.bilibili.com/x/activity/bws/online/park/reserve/do"
        data = {
            "ticket_no": ticket_no,
            "csrf": self.csrf_token,
            "inter_reserve_id": inter_reserve_id,
            "statistics":{"appId":1,"platform":3,"version":"8.52.0","abtest":""}

        }
        try:
            res_info = self.session.post(url, headers=self.headers, cookies=self.cookies, data=data)
            if res_info.status_code == 200:
                return res_info.json()
            else:
                print(f"请求失败，状态码：{res_info.status_code}")
                return False
        except requests.exceptions.Timeout:
            print("请求超时，请检查网络或尝试重试")
        except requests.exceptions.ConnectionError:
            print("连接失败，无法连接到服务器，请检查网络或URL是否正确")
        except requests.exceptions.RequestException as e:
            print(f"请求发生未知错误: {e}")
        except Exception as e:
            print(f"非请求相关的异常: {e}")
        return False
