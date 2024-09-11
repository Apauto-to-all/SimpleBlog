from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Form,  # 功能：用于获取表单数据
    Request,
    Cookie,  # 功能：用于操作 Cookie
    Response,  # 功能：用于返回响应
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

# 引入验证码模块
import random
from captcha.image import ImageCaptcha
import string  # 导入 string 模块，用于生成验证码


import logging

from utils import login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/user_login", response_class=HTMLResponse)
async def login(
    request: Request,
    access_token: Optional[str] = Cookie(None),
):
    if access_token and await login_util.is_login(access_token):
        return templates.TemplateResponse(
            "login.html", {"request": request, "is_login": True}
        )
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/user_login")
async def login(
    username: Optional[str] = Form(""),  # 获取用户名
    password: Optional[str] = Form(""),  # 获取密码
    captcha: Optional[str] = Form(""),  # 获取验证码
    remember: Optional[str] = Form(""),  # 获取记住我
    captcha_token: Optional[str] = Cookie(None),  # 获取验证码的 token
):
    logger.info("发送登入请求")
    # 验证码验证
    if not await login_util.verify_password(captcha_token, captcha.lower()):
        return {"error": "验证码错误"}
    # 要求
    limit = """登入失败，用户名或密码错误"""
    if await login_util.login_user(username, password):
        # 添加cookie
        response = RedirectResponse(f"/user/{username}", status_code=302)
        if remember == "on":
            logger.info("选择记住我，设置 Cookie 过期时间")
            response.set_cookie(
                key="access_token",  # 设置 Cookie 的键
                value=await login_util.get_access_jwt(username),  # 设置 Cookie 的值
                max_age=60 * login_util.login_time_minute,  # 设置 Cookie 的过期时间
            )
        else:
            response.set_cookie(
                key="access_token",  # 设置 Cookie 的键
                value=await login_util.get_access_jwt(username),  # 设置 Cookie 的值
            )
        return response
    return {"error": str(limit)}


@router.get("/user_register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/user_register")
async def register(
    username: Optional[str] = Form(""),  # 获取用户名
    password: Optional[str] = Form(""),  # 获取密码
    confirm_password: Optional[str] = Form(""),  # 获取确认密码
    nickname: Optional[str] = Form(""),  # 获取昵称
    captcha: Optional[str] = Form(""),  # 获取验证码
    captcha_token: Optional[str] = Cookie(None),  # 获取验证码的 token
):
    # 要求
    limit = """
    用户名不能重复且只能包含字母和数字，
    用户名长度为2-15，
    密码长度为4-15，
    昵称长度为2-20
    """
    logger.info("发送注册请求")
    # 验证码验证
    if not await login_util.verify_password(captcha_token, captcha.lower()):
        return {"error": "验证码错误"}
    if await login_util.register_user(username, password, confirm_password, nickname):
        logger.info("注册成功，重定向到登入页面")
        response = RedirectResponse("/user_login", status_code=302)
        # 删除登入的 Cookie
        response.delete_cookie(key="access_token")
        return response
    return {"error": str(limit)}


# 注销页面
@router.get("/user_logout")
async def logout():
    response = RedirectResponse("/index", status_code=302)
    response.delete_cookie(key="access_token")
    return response


# 获取验证码API
@router.get("/get_captcha")
async def get_captcha():
    image_captcha = ImageCaptcha()  # 创建图片验证码对象
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=4)
    )  # 生成随机验证码, 长度为 4，包含大写字母和数字
    data = image_captcha.generate(captcha_text)  # 生成图片验证码
    data.seek(0)  # 移动指针到文件开头
    response = Response(content=data.read(), media_type="image/png")  # 创建响应对象
    captcha_text = captcha_text.lower()  # 将验证码转换为小写
    response.set_cookie(
        key="captcha_token", value=await login_util.encrypt_password(captcha_text)
    )  # 设置 cookie，存储加密后的验证码
    return response  # 返回图片验证码
