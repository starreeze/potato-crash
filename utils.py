# coding=utf-8
import user
from bs4 import BeautifulSoup as bs
import requests, time


head = {
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    "Host": "elite.nju.edu.cn",
    #'Referer': 'http://elite.nju.edu.cn/jiaowu/student/elective/gymClassList.do',
    "Origin": "http://elite.nju.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Cookie": user.cookie,
}


def process_cmd(cmdList):
    optList = []
    i = 0
    while i < len(cmdList):
        if cmdList[i][0] == "-":
            optList.append(cmdList[i][1:])
            del cmdList[i]
        else:
            if len(cmdList[i]) == 1 and cmdList[i][0] == "_":
                cmdList[i] = ""
            i += 1
    if cmdList[0] == "exit":
        exit(0)
    return cmdList, optList


def get_cmd_stdin():
    s = input(">> ")
    cmdList = s.split(" ")
    while any(len(cmd) == 0 for cmd in cmdList):
        print("Invalid command.")
        s = input(">> ")
        cmdList = s.split(" ")
    return process_cmd(cmdList)


# get an url, retry forever if fail
def get(url, timeout=6, interval=0.2):
    while True:
        try:
            r = bs(requests.get(url, headers=head, timeout=timeout).content, "lxml")
            break
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
        ):
            time.sleep(interval)
    return r


# post an url with data, retry forever if fail
def post(url, data, timeout=6, interval=0.2):
    while True:
        try:
            r = bs(
                requests.post(url, data=data, headers=head, timeout=timeout).content,
                "lxml",
            )
            break
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
        ):
            time.sleep(interval)
    return r
