import requests
import datetime, time
import cookieM
import ntplib
from BiliBili import BiliBili
def t_to_d(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def time_check():
    time_offset = 0
    c = ntplib.NTPClient()
    skip = False
    try:
        response = c.request('ntp.aliyun.com')
    except Exception:
        print("时间同步出现错误，将跳过时间检查")
        skip = True
    if skip == False:
        time_offset = response.offset

    print(f"当前时间偏移：{time_offset:.2f}秒")
    return time_offset

def get_time():
    return int(time.time() + time_offset)


print(
    'BW乐园，启动喵~'
)

bw_park = BiliBili(cookieM.load_cookie())
bws_info = bw_park.bws_info()

# err exit
if not bws_info:
    print('账号信息错误或异常，请检查 网络/账号/Cookies 再试，详细报错见上方 err。')
    exit()

ticket_days = list(bws_info['user_reserve_info'].keys())
ticket_id = {}
reserve_dict = {}

print("主人的BW票票喵：")
for row in ticket_days:
    ticket_id[row] = bws_info['user_ticket_info'][row]['ticket']
    print(
        f"{bws_info['user_ticket_info'][row]['screen_name']} | 票种：{bws_info['user_ticket_info'][row]['sku_name']} | 电子票号：{bws_info['user_ticket_info'][row]['ticket']}")


for row in ticket_days:
    # print(
    #     f"{bws_info['user_ticket_info'][row]['screen_name']} | 票种：{bws_info['user_ticket_info'][row]['sku_name']} | 电子票号：{bws_info['user_ticket_info'][row]['ticket']}"
    # )

    for reserve in bws_info['reserve_list'][row]:
        title = reserve['act_title'].replace('\n', '')
        reserve_dict[reserve['reserve_id']] = [title, reserve['act_begin_time'], reserve['reserve_begin_time']]
    #     print(f"活动代码：{reserve['reserve_id']}  {title} 预约：{t_to_d(reserve['reserve_begin_time'])} 开始：{t_to_d(reserve['act_begin_time'])}")
    # print("\n")

time_offset = time_check()

preTime = 0
print(f'preTime设置{preTime}喵')

reserve_id_list = []
while(True):
    in_id = input('该输入活动代码了喵（输入0结束退出喵~）：')
    if int(in_id) ==0:
        break
    if int(in_id) not in reserve_dict:
        print('选择不正确！')
        continue

    reserve_id_list.append(int(in_id))
    print(f'{in_id}：{reserve_dict[int(in_id)][0]} 已选中')
    print()

print("准备开始抢票了喵~")

for i in reserve_id_list:
    print(f'{str(i)}：{reserve_dict[i][0]} 已选中')

for i in reserve_id_list:
    # 单个活动
    days = datetime.datetime.fromtimestamp(reserve_dict[i][1]).strftime("%Y%m%d")
    ticket_no = ticket_id[days]
    inter_reserve_id = i
    gap_time = 0
    print(f'{str(i)}：{reserve_dict[i][0]} 喵~')
    while get_time() < reserve_dict[i][2] - preTime:
        if get_time() + 60 < reserve_dict[i][2]:
            if get_time() > gap_time + 60:
                gap_time = get_time()
                print(f'等待开票……当前优先预约：{reserve_dict[i][0]} | 剩余：{reserve_dict[i][2] - get_time()}秒')
            time.sleep(3)
        elif get_time() > gap_time:
            gap_time = get_time()
            print(f'等待开票……当前优先预约：{reserve_dict[i][0]} | 剩余：{reserve_dict[i][2] - get_time()}秒')

    while get_time() <= reserve_dict[i][2] + 10:
        res = bw_park.bws_do(ticket_no, inter_reserve_id)
        if res == False:
            time.sleep(1)
            continue
        print(f"{print(t_to_d(get_time()))}请求结果喵~{res}")
        if res["code"] == 0:
            print("WINWIN了喵")
            print(f'编号{res["data"]["reserve_no"]}')
            break
        elif res["code"] == 1:
            print("好像已经抢到了喵~")
            break
        elif res["code"] == 75574:
            print("输光光了喵~")
            break
        elif res["code"] == 75637:
            print("好像没到时间哦~")
            # break
        elif res["code"] == -702:
            print("太快了喵~")
            time.sleep(0.85)
            continue
        time.sleep(0.8)

    time.sleep(0.8)

print("结束了喵~")

