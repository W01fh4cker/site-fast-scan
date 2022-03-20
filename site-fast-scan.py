print("""
@Author:w01f
@github:https://github.com/W01fh4cker
@version 1.0
@2022/3/18
___          ______          ___        ________         ____          _______
\  \        /  /\  \        /  /      /   ____  \       |   |         /  ____/
 \  \      /  /  \  \      /  /       |  |   |  |       |   |     __/   /___
  \  \    /  /    \  \    /  /        |  |   |  |       |   |    /___   ___/
   \  \  /  /      \  \  /  /         |  |   |  |       |   |       |  |
    \  \/  /        \  \/  /          |  |___|  |       |   |       |  |
     \____/          \____/           \ ________/       |___|       |__|
""")
import socket
import os
import time
import sys
import whois
import requests
# ip查询
print('[*]IP查询开始')
def ip_check(url):
    ip = socket.gethostbyname(url)
    print(ip)
    print('[*]IP查询完毕')
# whois查询
print('[*]whois信息查询开始')
def whois_check(url):
    data = whois.whois(url)
    print(data)
    print('[*]whois信息查询完毕')
# CDN判断-利用返回IP条数进行判断
def cdn_check(url):
    print('[*]CDN信息查询开始')
    ns = "nslookup " + url
    # data=os.system(ns)
    # print(data) #结果无法读取操作
    data = os.popen(ns, "r").read()
    if data.count(".") > 8:
        print("存在CDN")
    else:
        print("不存在CDN")
    print('[*]CDN信息查询完毕')
#子域名查询
def zym_list_check(url):
    print('[*]子域名信息查询开始')
    url = url.replace("www.", "")
    for zym_list in open("dic.txt"):
        zym_list = zym_list.replace("\n", "")
        zym_list_url = zym_list + "." + url
        try:
            ip = socket.gethostbyname(zym_list_url)
            print(zym_list_url + "->" + ip)
            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)
    print('[*]子域名信息查询完毕')
# 端口扫描
def port_check(url):
    print('[*]端口扫描开始')
    ip = socket.gethostbyname(url)
    ports = ["21","22","135","443","445","80","1433","3306","3389","1521","8000","7002","7001","8080","9090","8089","4848","8888","888","66","77"]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in ports:
        data = server.connect_ex((ip,int(port)))
        if data == 0:
            print(ip + ":" + port + "-->open")
        else:
            print(ip + ":" + port + "-->close")
    print('[*]端口扫描完毕')
# 系统判断
# 1.基于TTL值进行判断
# 2.基于第三方脚本进行判断
def os_check(url):
    print('[*]系统判断开始')
    data = os.popen("nmap\\nmap -O " + url, "r").read()
    print(data)
    print('[*]系统判断完毕')
if __name__ == '__main__':
    print("用法示例：python site-fast-scan.py www.baidu.com all")
    url = sys.argv[1]
    check = sys.argv[2]
    # print(url +"\n"+ check)
    if check == "all":
        ip_check(url)
        whois_check(url)
        port_check(url)
        cdn_check(url)
        os_check(url)
        zym_list_check(url)
