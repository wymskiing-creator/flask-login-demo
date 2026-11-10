# Flask 登录学习项目

基于 Python、Flask 和 Jinja2 的课程实验，在 AI 辅助下完成，正在用于学习 Web 请求处理与 GitHub 版本管理。

## 功能

- 首页、登录页及页面跳转
- 固定教学账号校验、空值与错误提示
- session 登录状态和退出登录
- POST 登录与 GET 参数传递教学演示

没有注册或数据库功能。账号定义在 app.py 的 DEMO_USER 中。

## 本地运行（PowerShell）

在本文件所在目录打开终端，依次执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

浏览器访问 http://127.0.0.1:5050/ 。教学账号：admin；密码：123456。
关闭服务：回到终端按 Ctrl+C。

## 项目结构

```text
app.py              Flask 路由、账号校验、会话处理
verify.py           自动验证脚本
requirements.txt    依赖
.gitignore          Git 忽略规则
templates/          HTML 页面和 Jinja2 模板
static/             CSS 样式
```

## 登录流程

浏览器提交表单 → /login 读取参数 → 校验固定账号和密码 → 写入 session → 跳转首页 → 模板显示欢迎信息。
POST 表单由 request.form 读取；GET 演示由 request.args 读取。

## 验证

```powershell
.\.venv\Scripts\python.exe verify.py
```

验证结果写入本地的“验证结果.txt”，不纳入 Git。脚本覆盖页面响应、静态资源、错误输入、登录、退出和跳转；浏览器视觉效果需另外检查。

## 教学边界

GET 演示会将密码放入网址，仅用于固定教学账号。真实登录应使用 POST 与 HTTPS。本项目开启了本地调试，不作为线上认证系统使用。
Flask 默认 session 使用签名 Cookie，签名用于防篡改，不表示内容被加密；不要存放密码。

## 学习任务

- [ ] 在本地打开首页并完成一次登录和退出
- [ ] 找到 app.py 中的 index 和 login 函数
- [ ] 修改首页一句文字，刷新确认效果
- [ ] 将源码上传自己的 GitHub 仓库
- [ ] 使用分支和 Pull Request 完成下一次修改
