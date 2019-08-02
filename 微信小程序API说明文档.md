# 本网站微信小程序的API说明文档（所有入口已被关闭）

## 1 验证码图片
- 网址：/BPlan/verificationCode/get/
- 请求方式：GET
- 返回一张验证码的图片，返回方式是HTTPResponse
- 示例：
1. img标签：
    ```html
    <img class="code" alt="验证码" onclick="refreshSrc()"/>
    ```
2. js代码：
    ```js
    function refreshSrc(){  //刷新验证码图片
        document.getElementsByClassName('code')[0].setAttribute('src', "/BPlan/verificationCode/get/?" + new Date().getTime());
    }
    ```
3. jQuery代码：
    ```js
    function refreshSrc(){  //刷新验证码图片
        $('.code').attr('src', "/BPlan/verificationCode/get/?" + new Date().getTime());
    }
    ```
4. 【注意】：每次加载页面时先执行refreshSrc函数
## 2 用户登录
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

## 3 注销
- 网址：/BPlan/wx/logout/
- 请求方式：GET
- 请求的参数：
```json
{"wx_AppId": "微信小程序的ID"}
```
- 返回方式：Json
- 返回的参数：
```json
{"status": ""}
```
|参数名称|可能出现的结果|释义
|---|---|---|
|status|success|注销成功
| |fail|注销失败|
- 请求示例：
```http request
..../BPlan/wx/logout/
```
- 返回示例：
```html
{"status": "success"}
```
