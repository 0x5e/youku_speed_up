#!/usr/bin/env python
# coding=utf-8

passport = '15000000000'
password = '000000'

import requests
import json
import re
import hashlib
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

session = requests.session()

actions = {
	# 'getConfig': 'http://account.youku.com/getConfig.json',
	'refreshFormToken': 'http://account.youku.com/refreshFormToken.json',
	'login': 'http://account.youku.com/login/confirm.json',

	# http://static.youku.com/paymentcenter/vip-pc/build/js/libs/config-build.js
	'speed_up': 'http://vip.youku.com/?c=ajax&a=ajax_do_speed_up', # 宽带加速
	'switch_service_url': 'http://vip.youku.com/?c=ajax&a=ajax_speedup_service_switch', # 加速服务开关
	'speed_status': 'http://vip.youku.com/ajax/speedup/get_status.jsonp', # 用户的宽带加速状态判断
}

def loads_jsonp(_jsonp):
	return json.loads(re.match('.*?({.*}).*', _jsonp, re.S).group(1))

def login():
	response = session.get(actions['refreshFormToken'])
	token = loads_jsonp(response.text)['data']['formtoken']
	logging.debug(token)

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
	data = loads_jsonp(response.text)
	if data['result'] == 'success':
		logging.info(u'登录成功')
		return True
	else:
		logging.info(data['errorMsg'])
		return False

def get_status():
	response = session.get(actions['speed_status'])
	data = loads_jsonp(response.text)['result']
	return data

def speed_up():
	response = session.get(actions['speed_up'])
	data = response.json()
	logging.info(data['msg'])
	if 'operator_error_msg' in data['result']:
		logging.info(data['result']['operator_error_msg'])

def switch():
	response = session.get(actions['switch_service_url'])
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
	main()
