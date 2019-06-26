from user_agents import parse
import json
from urllib.request import urlopen
import urllib


def get_agent(request):
    """返回代理信息（浏览器，系统，设备）"""
    us_str = request.META['HTTP_USER_AGENT']
    user_agents = parse(us_str)
    browser = user_agents.browser.family+user_agents.browser.version_string
    system = user_agents.os.family+user_agents.os.version_string
    device = user_agents.device.family
    if device == 'Other':
        if user_agents.is_mobile is True:
            device = '移动设备'
        elif user_agents.is_pc is True:
            device = 'PC端'
        elif user_agents.is_tablet is True:
            device = '平板电脑'
        else:
            device = '未知的设备'
    return {
        'browser': browser,
        'system': system,
        'device': device,
    }


def get_location(ip):
    """返回位置信息"""
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip='+ip
    error_flag = True
    while error_flag:  # 循环，直到请求成功
        try:
            ul_response = urlopen(url, timeout=1000)
            error_flag = False
        except urllib.request.HTTPError:
            error_flag = True
    location = json.loads(ul_response.read().decode('utf-8'))
    country = location['data']['country']  # 国家
    area = location['data']['area']  # 地区
    region = location['data']['region']  # 省份
    city = location['data']['city']  # 城市
    isp = location['data']['isp']  # 运营商
    ip_location = country+area+region+city+isp
    return ip_location


def get_ip(request):
    """返回当前用户的ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip


def whether_mobile(request):
    """判断是否为移动设备"""
    us_str = request.META['HTTP_USER_AGENT']
    user_agents = parse(us_str)
    return user_agents.is_mobile
