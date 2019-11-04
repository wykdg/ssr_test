import re
import threadpool
import subprocess
import sys
import urllib

import requests

import ParseSsr
from apply_route import apply


def get_subscribe(url):
    ssr_config=[]
    speed_result=[]
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    f=urllib.request.Request(url,headers=headers)

    ssr_subscribe = urllib.request.urlopen(f).read().decode('utf-8') #获取ssr订阅链接中数据
    ssr_subscribe_decode = ParseSsr.base64_decode(ssr_subscribe)
    ssr_subscribe_decode=ssr_subscribe_decode.replace('\r','')
    ssr_subscribe_decode=ssr_subscribe_decode.split('\n')

    for i in ssr_subscribe_decode:
        if(i):
            decdata=str(i[6:])#去掉"SSR://"
            ssr_config.append(ParseSsr.parse(decdata))#解析"SSR://" 后边的base64的配置信息返回一个字典
    return ssr_config

urls=[("国内网站","http://ip.6655.com/ip.aspx?area=1"),
      ("国外网站","http://bot.whatismyipaddress.com/"),
      ("谷歌","http://ip-goji.appspot.com/text")]
def check_route_ssr():


    for  name,url in urls:
        rsp=requests.get(url, timeout=5)
        print(name,rsp.text)


def check_http(ssr, ssr_port, network_timeout=1):
    cmd = "python ./shadowsocks/local.py -qq -s %s -p %s -k %s -m %s -O %s -o %s -g %s -G %s -b %s -l %s " % (
        ssr['server'], ssr['port'], ssr['password'], ssr['method'], ssr['protocol'], ssr['obfs'], ssr["obfsparam"],
        ssr["protoparam"], "127.0.0.1", ssr_port)
    # print(cmd)
    ip=None
    try:
        x = subprocess.Popen(cmd)

        my_proxies = {"http": "socks5://127.0.0.1:%s" % ssr_port, "https": "socks5://127.0.0.1:%s" % ssr_port}
        try:

            ip = requests.get('http://api.ip.sb/ip', timeout=network_timeout, proxies=my_proxies).text.strip()

        except Exception as e:
            pass
            # print(e.args)
        x.kill()
    except Exception as e:
        # print (e.args)
        pass
    return ip



def check_delay(host):
    try:
        ret = subprocess.Popen("ping -n 3 %s" % host, shell=True, stdout=subprocess.PIPE)
        out = ret.stdout.readlines()
        pattern = re.compile(r'\d+')
        # pattern=re.compile(r'= .?ms')
        ping_pc = pattern.findall(out[-1].decode('gbk'))
        # print("ping_test,localPing:", ping_pc[-1])
        return int(ping_pc[-1])
    except:
        pass
    return None
network_timeout=3
def run_test(ssr,ssr_port):
    
    # =args
    name=ssr["remarks"]
    ip=check_http(ssr,ssr_port,network_timeout)
    if ip:
        ping=check_delay(ssr['server'])
    else:
        ping=None
    return name,ip,ping
def close_ssr():
    subprocess.call('taskkill /f /im local.py',stdout=subprocess.PIPE)
result=[]
def callback(request,response):
    name, ip, ping=response
    if ip and ping:
        result.append((response))
def update_route_ssr(server_type, subscribe_url,route_ip):
    ssr_config = get_subscribe(subscribe_url)
    close_ssr()
    port=12000
    poolsize=16
    args=[]

    config_dict={}
    for config in ssr_config:
        server_name=config["remarks"]
        if server_name[:2] not in server_type:
            continue
        config_dict[server_name]=config
        args.append(((config,port),None))
        port+=1
    pool = threadpool.ThreadPool(poolsize)
    reqs = threadpool.makeRequests(run_test, args, callback)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    result.sort(key=lambda x:x[2])
    for name,ip,ping in result:
        print(name,"%dms"%ping)

    config1=config_dict[result[0][0]]
    config2=config_dict[result[1][0]]

    apply(config1,config2,route_ip)

if __name__ == '__main__':
    route_ip="192.168.123.1"
    server_type = ["V2"]
    subscribe_url=sys.argv[1]
    update_route_ssr(server_type, subscribe_url,route_ip)
    check_route_ssr()