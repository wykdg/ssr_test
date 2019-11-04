import urllib

import requests


req=requests.Session()
def apply(config1, config2,route_ip):
    url = "http://%s/start_apply.htm"%route_ip
    host1, port1, key1,method1= config1["server"], config1["port"], config1["password"], config1["method"]

    params1="-O %s -o %s -g %s -G %s " % (
        config1['protocol'], config1['obfs'], config1["obfsparam"], config1["protoparam"])

    if config2 is None:
        config2=config1


    host2, port2, key2,method2= config2["server"], config2["port"], config2["password"],config2["method"]
    params2 = "-O %s -o %s -g %s -G %s " % (
        config2['protocol'], config2['obfs'], config2["obfsparam"], config2["protoparam"])


    content={
        "current_page": "/",
        "next_page": "device-map/ss.asp",
        "next_host": "",
        "sid_list": "DeviceSecuritySS;LANHostConfig;General;",
        "group_id": "rt_ACLList",
        "action_mode": "Apply ",
        "action_script": "",
        "ss_change_2_ss_method": "0",
        "rt_ssnum_x_0": "54",
        "ss_run_ss_local": "",
        "ss_enable": "1",
        "ss_mode_x": "0",
        "ss_type": "1",
        "ssr_link": "https//subscribe2.kantianxia.eu.org/link/3ItPYiCQVhwM2GNe?sub=1",
        "ss_link_status": "8c53d5a1d39abd23721630150aa9b9c7",
        "rt_ssnum_x_tmp": "https//subscribe2.kantianxia.eu.org/link/3ItPYiCQVhwM2GNe?sub=1",
        "ssr_ss_link": "",
        "ssr_type_protocol": "auth_chain_b",
        "ssr_type_obfs": "http_simple",
        "rt_ss_name_x_0": "",
        "rt_ss_server_x_0": "",
        "rt_ss_port_x_0": "",
        "rt_ss_password_x_0": "",
        "rt_ss_method_x_0": "",
        "rt_ss_method_write_x_0": "",
        "rt_ss_usage_x_0": "-O auth_chain_b  -o http_simple",
        "ping_ss_x_0": "",
        "ping_txt_x_0": "",
        "ss_server": host1,
        "ss_server2": host2,
        "ss_server_port":port1,
        "ss_s2_port": port2,
        "ss_key":key1,
        "ss_s2_key": key2,
        "ss_method": method1,
        "ss_s2_method": method2,
        "ss_usage": params1,
        "ss_s2_usage": params2,
    }
    headers={"Host":route_ip,
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "Authorization":"Basic YWRtaW46dGVtcHVzZXI=",
            "Origin":"http://%s" %route_ip,
            "Upgrade-Insecure-Requests":"1",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer":"http://%s/device-map/ss.asp"%(route_ip),
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cookie":"n56u_cookie_hist_scale=1",}

    # x="&".join(["%s=%s"%(k,v) for k,v  in content.items()])
    content=urllib.parse.urlencode(content)
    # print(content)
    rsp=req.post(url,data=content,headers=headers)
    print("更新成功")
    # print(rsp.text)