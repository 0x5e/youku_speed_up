#!/usr/bin/env python
# coding=utf-8

import requests
import json
import time

def main():

	username = raw_input('用户名: ')
	password = raw_input('密码: ')

	session = requests.session()

	payload = {
		'passport': username,
		'password': password,
		'captcha': '',
		'remember': '1',
		'callback': 'logincallback_%d' % (time.time() * 1000),
		'from': 'http://login.youku.com/@@@@',
		'wintype': 'page',
	}
	response = session.post(url = 'https://login.youku.com/user/login_submit/', data = payload)
	print(response.text)

	response = session.post(url = 'http://vip.youku.com/?c=ajax&a=ajax_do_speed_up')
	print(json.dumps(response.json(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
	main()