# 本网站微信小程序的API说明文档

## 1 用户登录
- 网址：/BPlan/wx/login/
- 请求方式：GET
- 请求的参数：
```json
{
    "wx_AppId": "微信小程序的ID",
    "user_id": "账号",
    "user_password": "密码",
    "code": "验证码"
}
```
- 返回方式：Json
- 返回的参数：
```json
{
    "status": "",
    "information": ""
}
```
|参数名称|可能出现的结果|释义
|---|---|---|
|status|success|请求成功
| |fail|请求失败|
|information|idDoesNotExist|用户不存在|
| |successLogin|登录成功|
| |passwordWrong|密码错误|
| |codeWrong|验证码错误|
- 请求示例：
```http request
..../BPlan/wx/login/?wx_AppId=123456&user_id=000001&user_password=00000&code=cjht
```
- 返回示例
```json
{"status": "success", "information": "codeWrong"}
```
