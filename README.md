# 优酷宽带加速API（2017.7.1）

## 1.登录

### 1.1 获取表单Token

http://account.youku.com/refreshFormToken.json （或 http://account.youku.com/getConfig.json ）

返回值

```js
null({
    "data": {
        "formtoken": "B99D8D94C231583B742A7AF59BF8151B"
    },
    "errorCode": "",
    "errorMsg": "",
    "result": "success"
})
```

### 1.2 登录

http://account.youku.com/login/confirm.json

请求参数

```js
{
	"formtoken": formtoken,
	"passport": passport,
	"password": md5(password),
	"loginType": "passport_pwd",
	"UA": "FFFF00000000016514CE",
	"jsToken": "0"
}
```

返回值

```js
null({
    "errorCode": "",
    "errorMsg": "",
    "msg": {
        "domains": [
            "account.laifeng.com",
            "account.tudou.com",
            "account.soku.com",
            "account.youku.com"
        ]
    },
    "result": "success"
})
```

## 2.获取状态

http://vip.youku.com/ajax/speedup/get_status.jsonp

返回值

```js
callback({
    "code": "20000",
    "msg": "成功",
    "result": {
        "speed_up_state": false,
        "speed_up_switch": 1 # 1:开启, 2:关闭
    }
})
```

## 3.开启「加速服务开关」

http://vip.youku.com/?c=ajax&a=ajax_speedup_service_switch

返回值

```js
{
    "code": "20000",
    "msg": "成功",
    "result": {
        "state": "2"
    }
}
```

## 4.开启「宽带加速」

http://vip.youku.com/?c=ajax&a=ajax_do_speed_up

返回值

```js
// 成功

// 失败
{
    "code": "20023",
    "msg": "运营商繁忙",
    "type": "operator_not_range",
    "result": {
        "operator_error_code": 2001,
        "operator_error_msg": "中国电信提示：[2001]业务处理错误：用户线路暂不具备提速能力,加速ID:xxxxxxxxx"
    }
}
```

不要问我「加速服务开关」与「宽带加速」的区别，我可讲不清。。。
