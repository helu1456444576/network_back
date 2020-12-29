import logging
import telnetlib
import time
from web_Nat import Ping
from web_Nat import OpenWeb as web


class TelnetClient():
    def __init__(self, ):
        self.tn = telnetlib.Telnet()

    # 此函数实现telnet登录主机
    def login_host(self, host_ip, username, password):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip, port=23)
        except:
            logging.warning('%s网络连接失败' % host_ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'login: ', timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(1)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            # logging.warning('%s登录成功' % host_ip)
            print(host_ip + "登陆成功")
            return True
        else:
            # logging.warning('%s登录失败，用户名或密码错误' % host_ip)
            print(host_ip + "登录失败，用户名或密码错误")
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_command(self, command):
        result = ""
        for i in range(len(command)):
            # 执行命令
            self.tn.write(command[i].encode('ascii') + b'\n')
            time.sleep(1)
            # 获取命令结果
            command_result = self.tn.read_very_eager().decode('ascii')
            print(command_result)
            # logging.warning('命令执行结果：\n%s' % command_result)
            result += command_result
        return result

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"exit\n")


if __name__ == '__main__':
    host_ip = '220.110.0.2'
    username = 'HEY'
    password = 'CISCO'
    homework_command = ['enable', 'CISCO',
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
                        'ip nat inside source list 1 pool globalXYZ overload',]
    balance_command = ['no ip nat inside source list 1 pool globalXYZ overload',
                       'ip http server',
                       'ip nat pool tcppool 192.168.1.1 192.168.1.2 netmask 225.255.255.0 type rotary',
                       'access-list 2 permit host 220.110.0.60',
                       'ip nat inside destination list 2 pool tcppool']
    reuse_command = ['enable', 'CISCO',
                     'configure terminal',
                     'ip nat pool natpool 192.168.1.1 192.168.1.2 netmask 255.255.255.0',
                     'access-list 3 permit host 220.110.0.61',
                     'ip nat inside source list 3 pool natpool overload']
    test_command = ['end',
                    'show ip nat tr']
    telnet_client = TelnetClient()
    # 如果登录结果返加True，则执行命令，然后退出
    if telnet_client.login_host(host_ip, username, password):
        print("telnet success")
        homework_command_result = telnet_client.execute_command(homework_command)
        print("jlkjflsadkjflksadjflksajdflkajsdflksjflaksjd")
        print(homework_command_result)

        # ping_result = Ping.ping("192.168.1.10")
        # balance_command_result = telnet_client.execute_command(balance_command)
        # web.connect("220.110.0.60")
        # test_command_result = telnet_client.execute_command(test_command)
        # reuse_command_result = telnet_client.execute_command(reuse_command)
        # web.connect("220.110.0.61")
        # test_command_result2 = telnet_client.execute_command(test_command)
        # telnet_client.logout_host()
