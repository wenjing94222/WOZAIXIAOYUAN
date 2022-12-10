# -*- encoding:utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
import urllib
import urllib.parse
from urllib.parse import urlencode

import requests

import utils


class WoZaiXiaoYuanPuncher(utils.Data):
    def __init__(self):
        super().__init__(city=os.environ["WZXY_CITY"], address_recommend=os.environ["ADDRESS_RECOMMEND"])
        # 打卡结果
        self.status_code = 0
        # 登陆接口
        self.loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        # 请求头
        self.header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.13(0x18000d32) NetType/WIFI Language/zh_CN miniProgram",
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "2",
            "Host": "gw.wozaixiaoyuan.com",
            "Accept-Language": "en-us,en",
            "Accept": "application/json, text/plain, */*",
        }
        # 请求体（必须有）
        self.body = "{}"
        self.session = None

    # 登录
    def login(self):
        username, password = str(os.environ["WZXY_USERNAME"]), str(
            os.environ["WZXY_PASSWORD"]
        )
        url = f"{self.loginUrl}?username={username}&password={password}"
        self.session = requests.session()
        # 登录
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res["code"] == 0:
            print("使用账号信息登录成功")
            self.jwsession = response.headers["JWSESSION"]
            self.set_cache()
            return True
        else:
            print(res)
            print("登录失败，请检查账号信息")
            self.status_code = 5
            return False

    # 执行打卡
    def doPunchIn(self):
        print("正在打卡...")
        url = "https://student.wozaixiaoyuan.com/health/save.json"
        self.header["Host"] = "student.wozaixiaoyuan.com"
        self.header["Content-Type"] = "application/x-www-form-urlencoded"
        self.header["JWSESSION"] = self.jwsession
        cur_time = int(round(time.time() * 1000))
        sign_data = {
            "answers": '["0","1","0"]',  # 在此自定义answers字段
            "latitude": self.latitude,
            "longitude": self.longitude,
            "country": self.country,
            "city": self.city,
            "district": self.district,
            "province": self.province,
            "township": self.township,
            "street": self.street,
            "areacode": self.areacode,
            "towncode": self.towncode,
            "citycode": self.citycode,
            "timestampHeader": cur_time,
            "signatureHeader": hashlib.sha256(
                f"{self.province}_{cur_time}_{self.city}".encode(
                    "utf-8"
                )
            ).hexdigest(),
        }
        data = urlencode(sign_data)
        self.session = requests.session()
        response = self.session.post(url=url, data=data, headers=self.header)
        response = json.loads(response.text)
        # 打卡情况
        # 如果 jwsession 无效，则重新 登录 + 打卡
        if response["code"] == -10:
            print(response)
            print("jwsession 无效，将尝试使用账号信息重新登录")
            self.status_code = 4
            loginStatus = self.login()
            if loginStatus:
                self.doPunchIn()
            else:
                print(response)
                print("重新登录失败，请检查账号信息")
        elif response["code"] == 0:
            self.status_code = 1
            print("打卡成功")
        elif response["code"] == 1:
            print(response)
            print("打卡失败：今日健康打卡已结束")
            self.status_code = 3
        else:
            print(response)
            print("打卡失败")

    # 获取打卡结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 2:
            return "✅ 你已经打过卡了，无需重复打卡"
        elif res == 3:
            return "❌ 打卡失败，当前不在打卡时间段内"
        elif res == 4:
            return "❌ 打卡失败，jwsession 无效"
        elif res == 5:
            return "❌ 打卡失败，登录错误，请检查账号信息"
        else:
            return "❌ 打卡失败，发生未知错误，请检查日志"

    # 推送打卡结果
    def sendNotification(self):
        notifyTime = utils.getCurrentTime()
        notifyResult = self.getResult()

 
        if os.environ.get("DD_BOT_ACCESS_TOKEN"):
            # 钉钉推送
            DD_BOT_ACCESS_TOKEN = os.environ["DD_BOT_ACCESS_TOKEN"]
            DD_BOT_SECRET = os.environ["DD_BOT_SECRET"]
            timestamp = str(round(time.time() * 1000))  # 时间戳
            secret_enc = DD_BOT_SECRET.encode("utf-8")
            string_to_sign = "{}\n{}".format(timestamp, DD_BOT_SECRET)
            string_to_sign_enc = string_to_sign.encode("utf-8")
            hmac_code = hmac.new(
                secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
            ).digest()
            sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 签名
            print("开始使用 钉钉机器人 推送消息...", end="")
            url = f"https://oapi.dingtalk.com/robot/send?access_token={DD_BOT_ACCESS_TOKEN}&timestamp={timestamp}&sign={sign}"
            headers = {"Content-Type": "application/json;charset=utf-8"}
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"""⏰ {os.environ["WZXY_USERNAME"]}的我在校园打卡结果通知\n---------\n打卡项目：健康打卡\n\n打卡情况：{notifyResult}\n\n打卡时间: {notifyTime}"""
                },
            }
            r = requests.post(
                url=url, data=json.dumps(data), headers=headers, timeout=15
            ).json()
            if not r["errcode"]:
                print("消息经 钉钉机器人 推送成功！")
            else:
                print("dingding:" + str(r["errcode"]) + ": " + str(r["errmsg"]))
                print("消息经 钉钉机器人 推送失败，请检查错误信息")



if __name__ == "__main__":
    # 找不到cache，登录+打卡
    wzxy = WoZaiXiaoYuanPuncher()
    if not os.path.exists(".cache"):
        print("找不到cache文件，正在使用账号信息登录...")
        loginStatus = wzxy.login()
        if loginStatus:
            wzxy.doPunchIn()
        else:
            print("登陆失败，请检查账号信息")
    else:
        print("找到cache文件，尝试使用jwsession打卡...")
        wzxy.doPunchIn()
    wzxy.sendNotification()
