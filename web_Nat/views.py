from django.shortcuts import render
from django.http import HttpResponse
from web_Nat import RTA
from web_Nat import RTB
from web_Nat import Ping
from web_Nat import OpenWeb as web


host_ip_rta = '220.110.0.2'
host_ip_rtb = '10.0.0.1'
username = 'HEY'
password = 'CISCO'
dynamic_command = ['enable', 'CISCO',
                        'configure terminal',
                        'ip route 0.0.0.0 0.0.0.0 s0/0/0',
                        'int f0/0',
                        'ip nat inside',
                        'exit',
                        'int s0/0/0',
                        'ip nat outside',
                        'exit',
                        'access-list 1 permit 192.168.1.0 0.0.0.255',
                        'ip nat pool globalXYZ 220.110.0.33 220.110.0.57 netmask 255.255.255.0',
                        'ip nat inside source list 1 pool globalXYZ overload']
static_command = ['enable', 'CISCO',
                        'configure terminal',
                        'ip route 0.0.0.0 0.0.0.0 s0/0/0',
                        'int f0/0',
                        'ip nat inside',
                        'exit',
                        'int s0/0/0',
                        'ip nat outside',
                        'exit',
                        'ip nat inside source static 10.0.0.10 220.110.0.34']
balance_command = ['no ip nat inside source list 1 pool globalXYZ overload',
                       'ip http server',
                       'ip nat pool tcppool 192.168.1.1 192.168.1.2 netmask 225.255.255.0 type rotary',
                       'access-list 2 permit host 220.110.0.60',
                       'ip nat inside destination list 2 pool tcppool']
reuse_command = ['enable', 'CISCO','configure terminal',
                     'ip nat pool natpool 192.168.1.1 192.168.1.2 netmask 255.255.255.0',
                     'access-list 3 permit host 220.110.0.61',
                     'ip nat inside source list 3 pool natpool overload']
test_command = ['end','show ip nat tr']
static_test_command = ['ping 10.0.0.10']

rta_client =RTA.TelnetClient()
rtb_client =RTB.TelnetClient()

from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,"index.html")

def dynamic(request):
    """
    动态方法，rta的homework是动态，rtb的homework是静态的
    :param request:
    :return: 执行结果（字符串）
    """
    if rta_client.login_host(host_ip_rta,username,password):
        dynamic_result=rta_client.execute_command(dynamic_command)
        message = {"msg": dynamic_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Dynamic Error!"}
        return JsonResponse(message)


def dynamic_test(request):
    """
    动态方法测试
    :param request:
    :return: 测试结果（字符串）
    """
    if rta_client.login_host(host_ip_rta,username,password):
        ping_result=Ping.ping("192.168.1.10")
        message = {"msg": ping_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Dynamic Test Error!"}
        return JsonResponse(message)

def balance(request):
    """
    负载均衡方法
    :param request:
    :return: 执行结果（字符串）
    """
    if rta_client.login_host(host_ip_rta, username, password):
        balance_result = rta_client.execute_command(balance_command)
        message = {"msg": balance_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Balance Error!"}
        return JsonResponse(message)


def balance_test(request):
    """
    负载均衡方法测试
    :param request:
    :return: 测试结果（字符串）
    """
    if rta_client.login_host(host_ip_rta, username, password):
        web.connect("220.110.0.60")
        test_result = rta_client.execute_command(test_command)
        message = {"msg": test_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Balance Test Error!"}
        return JsonResponse(message)

def reuse(request):
    """
    地址复用方法
    :param request:
    :return: 执行结果（字符串）
    """
    if rta_client.login_host(host_ip_rta, username, password):
        reuse_result = rta_client.execute_command(reuse_command)
        message = {"msg": reuse_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Reuse Error!"}
        return JsonResponse(message)


def reuse_test(request):
    """
    地址复用方法测试
    :param request:
    :return: 测试结果（字符串）
    """
    if rta_client.login_host(host_ip_rta, username, password):
        web.connect("220.110.0.61")
        test_result = rta_client.execute_command(test_command)
        message = {"msg": test_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Reuse test error"}
        return JsonResponse(message)


def static1(request):
    """
    静态方法
    :param request:
    :return:执行结果（字符串）
    """
    print("到此一游")
    if rtb_client.login_host(host_ip_rtb,username,password):
        static_result = rtb_client.execute_command(static_command)
        print(static_result)
        message={"msg":static_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Static Error!"}
        return JsonResponse(message)

def static_test(request):
    """
    静态方法测试
    :param request:
    :return: 测试结果（字符串）
    """
    if rta_client.login_host(host_ip_rtb,username,password):
        ping_result = rta_client.execute_command(static_test_command)
        print(ping_result)
        rta_client.logout_host()  # rtb青结
        message = {"msg": ping_result}
        return JsonResponse(message)
    else:
        message = {"msg": "Static Test Error!"}
        return JsonResponse(message)

# def getInfo(request):
#     return JsonResponse({"msg":"jjjjj"})
