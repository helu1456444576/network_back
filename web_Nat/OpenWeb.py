# coding=gbk
import time
import webbrowser


def connect(url):
    webbrowser.open(url)
    time.sleep(3)
    # 关闭谷歌浏览器，
    # os.system('taskkill /IM chrome.exe')

# connect("www.baidu.com")
