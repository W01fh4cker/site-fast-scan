from multiprocessing.dummy import Pool as ThreadPool
import socket
import os
import time
import sys
import whois
import requests
from datetime import datetime

socket.setdefaulttimeout(0.5) #设置超时为0.5秒
ports_all = []
# ip查询
print('[*]IP查询开始')
def ip_check(url):
    try:
        ip = socket.gethostbyname(url)
        print(ip)
        print('[*]IP查询完毕')
    except:
        print("[*]不存在该IP！")
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
# 端口扫描
# 指定端口扫描
def port_check_part(url):
    print('[*]指定端口扫描开始')
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
# 全端口扫描
def port_all_scan(port):
    server_ip = socket.gethostbyname(url)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = s.connect_ex((server_ip, int(port)))
        if res == 0:
            print(server_ip + ":" + port + "-->open")
        else:
            print(server_ip + ":" + port + "-->close")
    except:
        pass
def port_check_all(url):
    print('[*]全端口扫描开始')
    for i in range(1, 65536):  # 全端口扫描
        ports_all.append(i)
    time_start = datetime.now()
    pool = ThreadPool(processes = 1000) #设置线程池为1000
    results = pool.map(port_all_scan,ports_all)
    pool.close()
    pool.join()
    print('本次扫描用时%s' % (datetime.now() - time_start))
    print('[*]全端口扫描完毕')
if __name__ == '__main__':
    print("用法示例：python site-fast-scan.py www.baidu.com all")
    url = sys.argv[1]
    check = sys.argv[2]
    if check == "all":
        ip_check(url)
        whois_check(url)
        port_check_all(url)
        cdn_check(url)