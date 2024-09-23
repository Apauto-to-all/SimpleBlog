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


@router.post("/register/api")
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
        response = RedirectResponse("/login", status_code=302)
        # 删除登入的 Cookie
        response.delete_cookie(key="access_token")
        return response
    return {"error": str(limit)}
