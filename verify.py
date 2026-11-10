"""运行 python verify.py，验证模板、表单、会话与跳转。"""
from pathlib import Path
from app import app

app.config.update(TESTING=True)
checks = []


def check(condition, name):
    assert condition, name
    checks.append(name)


with app.test_client() as client:
    r = client.get('/')
    check(r.status_code == 200 and '进入登录页' in r.text, '未登录首页')
    r = client.get('/login')
    check(r.status_code == 200 and 'method="post"' in r.text and 'method="get"' in r.text,
          'GET 打开双表单页面')
    check('{{' not in r.text and '{%' not in r.text, 'Jinja2 已渲染')
    check(client.get('/static/style.css').status_code == 200, '静态 CSS 可读取')
    r = client.get('/welcome')
    check(r.status_code == 303 and r.location.endswith('/login'), '未登录不能进入欢迎页')
    for method in ['POST', 'GET']:
        for data, message in [({}, '用户名和密码都不能为空'),
                              ({'username': 'admin', 'password': 'bad'}, '用户名或密码错误'),
                              ({'username': 'other', 'password': '123456'}, '用户名或密码错误')]:
            if method == 'POST':
                r = client.post('/login', data=data, follow_redirects=True)
            else:
                r = client.get('/login', query_string=dict(data, submitted='1'), follow_redirects=True)
            check(message in r.text and '欢迎王一鸣同学回来' not in r.text, method + ' 校验：' + str(data.get('username', '空值')))
        data = {'username': ' admin ', 'password': '123456'}
        r = (client.post('/login', data=data) if method == 'POST' else
             client.get('/login', query_string=dict(data, submitted='1')))
        check(r.status_code == 303 and r.location == '/', method + ' 成功后跳转首页')
        r = client.get('/')
        check('欢迎王一鸣同学回来' in r.text and '登录成功' in r.text, method + ' 欢迎姓名与提示')
        check('<p>登录成功</p>' not in client.get('/').text, method + ' flash 只显示一次')
        check('欢迎王一鸣同学回来' in client.get('/').text, method + ' 刷新保留登录状态')
        client.post('/logout')
        check('欢迎王一鸣同学回来' not in client.get('/').text, method + ' 退出清除状态')
    r = client.get('/?name=伪造姓名')
    check('欢迎伪造姓名' not in r.text, '首页不信任查询参数中的姓名')
    check(client.get('/logout').status_code == 405, '退出仅接受 POST')
    check(client.get('/missing').status_code == 404, '不存在地址返回 404')

report = '\n'.join('PASS ' + name for name in checks)
report += f'\n\n共 {len(checks)} 项通过。\n验证方式：Flask test_client。浏览器显示效果需另行检查。\n'
Path(__file__).with_name('验证结果.txt').write_text(report, encoding='utf-8')
print(report)
