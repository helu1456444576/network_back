# coding=gbk
import time
import webbrowser


def connect(url):
    webbrowser.open(url)
    time.sleep(3)
    # �رչȸ��������
    # os.system('taskkill /IM chrome.exe')

# connect("www.baidu.com")
