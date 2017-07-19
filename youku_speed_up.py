#!/usr/bin/env python
# coding=utf-8

passport = '15000000000'
password = '000000'

import requests
import json
import re
import hashlib
import logging
import os
import pickle
import sys

log_switch = False #日志开关，True开，False关
log_path = os.path.join(os.path.expanduser("~"), 'Desktop') + '/' #日志路径，为win7+的桌面路径

if log_switch == True:
	logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=log_path+'log.txt', logging='a', level=logging.DEBUG)
else:
	logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

session = requests.session()
# session.headers = {
# 	'Referer': 'http://vip.youku.com/vips/priSpeedup.html',
# 	'User-Agent': 'Mozilla/5.0'
# }

actions = {
	# 'getConfig': 'http://account.youku.com/getConfig.json',
	'refreshFormToken': 'http://account.youku.com/refreshFormToken.json',
	'login': 'http://account.youku.com/login/confirm.json',

	# http://static.youku.com/paymentcenter/vip-pc/build/js/libs/config-build.js
	'get_member_info': 'http://vip.youku.com/ajax/member/get_member_info.jsonp', # 获取用户基本信息
	'speed_up': 'http://vip.youku.com/?c=ajax&a=ajax_do_speed_up', # 宽带加速
	'switch_service_url': 'http://vip.youku.com/?c=ajax&a=ajax_speedup_service_switch', # 加速服务开关
	'speed_status': 'http://vip.youku.com/ajax/speedup/get_status.jsonp', # 用户的宽带加速状态判断
}

def loads_jsonp(_jsonp):
	return json.loads(re.match('.*?({.*}).*', _jsonp, re.S).group(1))

def login():
	cookie_file_name = os.path.dirname(os.path.realpath(__file__)) + '/' + '%s.cookie'%passport
	if os.path.isfile(cookie_file_name):
		with open(cookie_file_name) as f:
			session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

	response = session.get(actions['speed_status'])
	logging.debug('Response: %s'%response.text)
	data = loads_jsonp(response.text)
	if data['code'] == '20000':
		return True

	logging.info(u'开始登陆')
	logging.info(data['msg'])
	session.cookies = requests.utils.cookiejar_from_dict({})

	response = session.get(actions['refreshFormToken'])
	logging.debug('Response: %s'%response.text)
	token = loads_jsonp(response.text)['data']['formtoken']

	m = hashlib.md5()
	m.update(password)
	md5_password = m.hexdigest()

	params = {
		'formtoken': token,
		'passport': passport,
		'password': md5_password,
		'loginType': 'passport_pwd',
		'UA': 'FFFF00000000016514CE',
		'jsToken': '0',
	}
	
	response = session.get(actions['login'], params = params)
	logging.debug('Response: %s'%response.text)
	data = loads_jsonp(response.text)
	if data['result'] == 'success':
		logging.info(u'登录成功')
		with open(cookie_file_name, 'w') as f:
		    pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
		return True
	else:
		logging.info(data['errorMsg'])
		return False

def get_status():
	response = session.get(actions['speed_status'])
	logging.debug('Response: %s'%response.text)
	data = loads_jsonp(response.text)['result']
	return data

def speed_up():
	response = session.get(actions['speed_up'])
	logging.debug('Response: %s'%response.text)
	data = response.json()
	logging.info(data['msg'])
	if 'operator_error_msg' in data['result']:
		logging.info(data['result']['operator_error_msg'])

def switch():
	response = session.get(actions['switch_service_url'])
	logging.debug('Response: %s'%response.text)
	data = response.json()
	logging.info(data['msg'])

def main():
	if login() == False:
		return

	status = get_status()
	if status['speed_up_state'] == True:
		logging.info(u'宽带加速已开启')
		return

	if status['speed_up_switch'] == 2:
		logging.info(u'开启[加速服务开关]...')
		switch()

	logging.info(u'开启[宽带加速]...')
	speed_up()

if __name__ == '__main__':
	#不加下面2句好像在win环境下会报错
	reload(sys)
	sys.setdefaultencoding('utf-8')
	main()
