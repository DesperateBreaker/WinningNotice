import datetime
import game
import email_send as my_email
import crawling_data as crawling
import sys
import json_read_write as js_rw

# 调试标志  release 分支改为 False
is_debug = True
basic_path = "/usr/src/python/WinGame/"

# data_path
if is_debug:
    data_path = "data.json"
    email_data_path = "email_data.json"
else:
    data_path = basic_path + data_path
    email_data_path = basic_path + email_data_path

# 设置发送邮件的相关参数
email_data = js_rw.read_json_file(email_data_path)
sender_email = email_data["sender_email"]
sender_password = email_data["sender_password"]
receiver_email_list = email_data["receiver_email_list"]
subject = "开奖信息"
body = ""


# 创建开奖通知信息
def crate_notice(notice_dict):
    notice1 = "【 {} 】：开奖期号：{},  恭喜您中 {} 等奖, 预计奖金为 {} 元。\n".format(notice_dict["name"], notice_dict["id"], notice_dict["win_level"], notice_dict["win_money"])
    
    today_num = "[" + ", ".join(map(str, notice_dict["today_num"])) + "]"
    my_num = "[" + ", ".join(map(str, notice_dict["my_num"])) + "]"
    notice2 = "今日开奖号码为: {}, 您的号码为: {}, ".format(today_num, my_num)
    
    prop_num = "[" + ", ".join(map(str, notice_dict["prop_num"])) + "]"
    back_num = "[" + ", ".join(map(str, notice_dict["back_num"])) + "]"
    notice3 = "其中, 前区中奖号码为: {}, 中了 {} 个, 后区中奖号码为 {}, 中了 {} 个。".format(prop_num, notice_dict["prop_status"], back_num, notice_dict["back_status"])

    return notice1 + notice2 + notice3


# 更新存储信息
def update_data(game_name, cur_id, bonus):
    data = js_rw.read_json_file(data_path)
    data[game_name]["curId"] = cur_id
    data[game_name]["bonus"] = data["ball"]["bonus"] + bonus
    js_rw.write_json_file(data_path, data)


# 判断是否需要发送购买梯形
# return1: Yes/No
# return: BuyInfo
def judge_buy_notice(game_name):
    data = js_rw.read_json_file(data_path)
    cur_id = int(data[game_name]["curId"])
    start_id = int(data[game_name]["startId"])
    period = int(data[game_name]["periods"])
    bonus = data[game_name]["bonus"]

    need_buy = False
    info = ""

    if (cur_id - start_id) >= period - 1:
        need_buy = True
        info = "您购买的 {} 期【 {} 】已于今日开奖完毕, 恭喜您累计中等奖 {} 元。\n".format(period, game_name, bonus)

    return need_buy, info


# main
if __name__ == '__main__':
    cur_date = datetime.date.today()

    weekday = cur_date.weekday() + 1    # 星期一: 1  ...  星期日: 7

    lotto_weekday = [1, 3, 6]           # lotto 开奖日
    ball_weekday = [2, 4, 7]            # ball  开奖日

    my_lotto_num1 = [4, 13, 16, 18, 23, 6, 11]
    my_lotto_num2 = [5, 8, 10, 20, 23, 2, 7]
    my_ball_num1 = [4, 7, 11, 16, 26, 31, 7]
    my_ball_num2 = [3, 4, 7, 8, 24, 28, 4]

    today_num = []
    today_issue = ""
    p_game1 = None
    p_game2 = None
    print("\n------------------ " + cur_date.strftime('%Y-%m-%d') + " ------------------")
    if weekday in lotto_weekday:
        print("lotto")
        p_game1 = game.LottoGame()
        p_game1.set_my_num(my_lotto_num1)
        p_game2 = game.LottoGame()
        p_game2.set_my_num(my_lotto_num2)
        p_crawling = crawling.LottoCrawling(0, 2)                    # 爬取 3 期数据
        today_num, today_issue = p_crawling.get_ball_num(0)          # 获取最新一期数据
    elif weekday in ball_weekday:
        print("ball")
        p_game1 = game.BallGame()
        p_game1.set_my_num(my_ball_num1)
        p_game2 = game.BallGame()
        p_game2.set_my_num(my_ball_num2)
        p_crawling = crawling.BallCrawling(0, 2)                     # 爬取 3 期数据
        today_num, today_issue = p_crawling.get_ball_num(0)          # 获取最新一期数据
    else:
        print("Not lotto and ball")
        sys.exit(0)

    # 设置当天中奖号码
    p_game1.set_today_num(today_num, today_issue)                 
    p_game2.set_today_num(today_num, today_issue)                 
    
    # 创建中奖信息
    win_info1 = p_game1.crate_win_info()                          
    win_info2 = p_game2.crate_win_info()

    # 创建开奖消息
    win_notice1 = crate_notice(win_info1)
    win_notice2 = crate_notice(win_info2)
    print(win_notice1 + win_notice2)

    # 更新存储信息(开奖期号、奖金)
    update_data(win_info1["name"], int(win_info1["id"]), win_info1["win_money"] + win_info2["win_money"])

    # 判断是否需要发送购买提醒
    needed_buy, buy_info = judge_buy_notice(win_info1["name"])
    if needed_buy:
        print(buy_info)

    # 发送信息
    if not is_debug:
        body = win_notice1 + win_notice2
        my_email.send_email(sender_email, sender_password, receiver_email_list, subject, message=body)          # 发送

        if needed_buy:
            subject = win_info1["name"] + "购买提醒"
            my_email.send_email(sender_email, sender_password, receiver_email_list, subject, message=buy_info)  # 发送

    # 邮件发送测试
    email_test = False
    if email_test:
        my_email.send_email(sender_email, sender_password, receiver_email_list, subject="Test", message="test")  # 发送



