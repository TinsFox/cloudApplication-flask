"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

import re
import time
import requests
from flask import current_app, jsonify, request
from lin.exception import ParameterException, AuthFailed


def get_timestamp(fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime(time.time()))


def get_count_from_query():
    count_default = current_app.config.get('COUNT_DEFAULT')
    count = int(request.args.get('count', count_default if count_default else 1))
    return count


def get_page_from_query():
    page_default = current_app.config.get('PAGE_DEFAULT')
    page = int(request.args.get('page', page_default if page_default else 0))
    return page


def paginate():
    _count = get_count_from_query()
    count = 15 if _count >= 15 else _count
    start = get_page_from_query() * count
    if start < 0 or count < 0:
        raise ParameterException()
    return start, count


def camel2line(camel: str):
    p = re.compile(r'([a-z]|\d)([A-Z])')
    line = re.sub(p, r'\1_\2', camel).lower()
    return line


def json_res(**kwargs):
    '''
    将所有传入的关键字参数转变为dict后序列化为json格式的response
    count, items, page, total, total_page ...
    '''
    return jsonify(kwargs)


def getAccessToken():
    APPSECET = current_app.config.get('APPSECET')
    appid = current_app.config.get('APPID')
    # url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=client_credential'
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'
    response = requests.get(url.format(appid, APPSECET))
    access_token = response.json()['access_token']
    expires = response.json()['expires_in']
    print(expires)
    return access_token


def getOpenID(code):
    APPSECET = current_app.config.get('APPSECET')
    appid = current_app.config.get('APPID')
    errcode = {
        '-1': u'系统繁忙，此时请开发者稍候再试',
        '40029': u'code无效',
        '45011': u'频率限制，每个用户每分钟100次',
    }
    response = requests.get(current_app.config.get('OPENIDURL').format(appid, APPSECET, code))
    response.encoding = response.apparent_encoding
    content = response.json()
    if 'errcode' in content.keys() and content.get('errcode') != 0:
        print(errcode[content.get('errcode')])
        raise AuthFailed(errcode[content.get('errcode')])
    return content


def request_wx_api(code):
    """
    # 请求微信接口　
    :param code: 用户登录凭证
    """
    app_secret = current_app.config.get('APPSECET')
    app_id = current_app.config.get('APPID')
    response = requests.get(current_app.config.get('OPENIDURL').format(app_id, app_secret, code))
    response.encoding = response.apparent_encoding
    content = response.json()
    if 'errcode' in content.keys() and content.get('errcode') != 0:
        raise AuthFailed(content.get('errmsg'))
    return content
