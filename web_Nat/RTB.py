import logging
import telnetlib
import time
from web_Nat import Ping


class TelnetClient():
    def __init__(self, ):
        self.tn = telnetlib.Telnet()
        self.login = False

    def get_login(self):
        return self.login

    # 此函数实现telnet登录主机
    def login_host(self, host_ip, username, password):
        if self.login:
            return True  # 已登录则直接返回
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
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager()
        print(type(command_result))
        command_result = command_result.decode('ascii')
        print(command_result)
        if 'Login incorrect' not in command_result:
            print(host_ip + "登陆成功")
            # logging.warning('%s登录成功' % host_ip)
            self.login = True
            return True
        else:
            print(host_ip + "登录失败，用户名或密码错误")
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_command(self, command):
        result = ""
        for i in range(len(command)):
            # 执行命令
            mycommand = command[i].encode('ascii')
            self.tn.write(mycommand + b'\n')
            # self.tn.write(command[i].encode('ascii'))
            time.sleep(3)
            # 获取命令结果
            command_result = self.tn.read_very_eager().decode('ascii').encode('utf-8')
            # print(command_result)
            # logging.warning('命令执行结果：\n%s' % command_result)
            result += command[i] + command_result
            logging.warning('%s登录失败，用户名或密码错误' % host_ip)
        print(result)
        return result

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"exit\n")


if __name__ == '__main__':
    host_ip = '10.0.0.1'
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
                        'ip nat inside source static 10.0.0.10 220.110.0.34']
    telnet_client = TelnetClient()
    # 如果登录结果返加True，则执行命令，然后退出
    if telnet_client.login_host(host_ip, username, password):
        print("telnet success")
        homework_command_result = telnet_client.execute_command(homework_command)
        ping_result = Ping.ping("220.110.0.34")
        telnet_client.logout_host()
