from user_agents import parse
import json
from urllib.request import urlopen
from ResearchAndTrainingBPlan.settings import PythonAnywhere
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
    if PythonAnywhere is True:
        url = 'http://ip-api.com/json/'+ip+'?fields=16409&lang=zh-CN'
        # ip地址查询的api，仅返回查询状态、国家、省、市，语言为汉语
        ul_response = urlopen(url, timeout=1000)
        location = json.loads(ul_response.read().decode('utf-8'))
        if location['status'] == 'fail':
            return '未知地址'
        country = location['country']  # 国家
        region = location['regionName']  # 省份
        city = location['city']  # 城市
        ip_location = country+region+city
        return ip_location
    else:
        return '本地地址'


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
