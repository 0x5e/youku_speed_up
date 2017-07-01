#!/usr/bin/env python
# coding=utf-8

passport = '15000000000'
password = '000000'

import requests
import json
import time
import re
import hashlib
import random
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

session = requests.session()
session.headers = {
	'Referer': 'http://vip.youku.com/vips/priSpeedup.html',
	'User-Agent': 'Mozilla/5.0'
}

def loads_jsonp(_jsonp):
	return json.loads(re.match('.*?({.*}).*', _jsonp, re.S).group(1))

def login():
	params = {
		'pid': '20160607PLF000287',
		'bizType': 'login',
		'jsonpCallback': '__jp0',
	}

	# response = session.get(url = 'http://account.youku.com/getConfig.json')
	response = session.get(url = 'http://account.youku.com/refreshFormToken.json', params = params)
	token = loads_jsonp(response.text)['data']['formtoken']
	logging.debug(token)

	m = hashlib.md5()
	m.update(password)
	md5_password = m.hexdigest()

	params = {
		'formtoken': token,
		'passport': passport,
		'password': md5_password,
		'buid': 'youku',
		'pid': '20160607PLF000287',
		'mode': 'popup',
		'sendCodeType': 'mobileCode',
		'state': 'false',
		'rememberMe': 'true',
		'loginType': 'passport_pwd',
		'UA': 'FFFF00000000016514CE:%s:%s'%(time.time() * 1000, random.random()),
		'jsToken': '0',
		'jsonpCallback': '__jp1',
	}
	
	response = session.get(url = 'http://account.youku.com/login/confirm.json', params = params)
	data = loads_jsonp(response.text)
	if data['result'] == 'success':
		logging.info('登录成功')
		return True
	else:
		logging.info(data['errorMsg'])
		return False

def get_status():
	response = session.get(url = 'http://vip.youku.com/ajax/speedup/get_status.jsonp')
	data = loads_jsonp(response.text)['result']
	return data

def speed_up():
	response = session.get(url = 'http://vip.youku.com/?c=ajax&a=ajax_do_speed_up')
	data = response.json()
	logging.info(data['msg'])
	if 'operator_error_msg' in data['result']:
		logging.info(data['result']['operator_error_msg'])

def switch():
	response = session.get(url = 'http://vip.youku.com/?c=ajax&a=ajax_speedup_service_switch')
	data = response.json()
	logging.info(data['msg'])

def main():
	if login() == False:
		return

	status = get_status()
	if status['speed_up_state'] == True:
		logging('加速服务已开启')
		return

	if status['speed_up_switch'] == 2:
		logging.info('开启[加速服务]...')
		switch()

	logging.info('开启[宽带加速服务]...')
	speed_up()

if __name__ == '__main__':
	main()
