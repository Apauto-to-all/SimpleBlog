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


@router.post("/login/api")
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
