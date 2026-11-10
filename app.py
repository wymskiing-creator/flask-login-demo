"""第四、五章课堂实验：模板、GET/POST 表单和登录跳转。"""
import os
import secrets

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# 固定教学账号；显示姓名由服务器提供，不信任网址中的姓名参数。
DEMO_USER = {"username": "admin", "name": "王一鸣",
             "password_hash": generate_password_hash("123456")}


@app.get("/")
def index():
    return render_template("index.html", name=session.get("name"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # 普通 GET 打开表单；带 submitted=1 的 GET 演示提交查询参数。
    if request.method == "GET" and request.args.get("submitted") != "1":
        return render_template("login.html")

    data = request.form if request.method == "POST" else request.args
    username = data.get("username", "").strip()
    password = data.get("password", "")
    session.clear()
    if not username or not password:
        flash("用户名和密码都不能为空")
        return redirect(url_for("login"), code=303)
    if username != DEMO_USER["username"] or not check_password_hash(
            DEMO_USER["password_hash"], password):
        flash("用户名或密码错误")
        return redirect(url_for("login"), code=303)

    session["name"] = DEMO_USER["name"]
    session["username"] = username
    session["login_method"] = request.method
    flash("登录成功")
    # 成功后跳转首页；登录状态下，首页即为欢迎页面。
    return redirect(url_for("index"), code=303)


@app.get("/welcome")
def welcome():
    # 欢迎页的备用入口同样检查登录状态。
    if "username" not in session:
        return redirect(url_for("login"), code=303)
    return redirect(url_for("index"), code=303)


@app.post("/logout")
def logout():
    session.clear()
    flash("已退出登录")
    return redirect(url_for("index"), code=303)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
