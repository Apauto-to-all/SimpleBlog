from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Form,  # 功能：用于获取表单数据
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/user/login", response_class=HTMLResponse)
async def login(
    request: Request,
    access_token: Optional[str] = Cookie(None),
):
    if access_token and await login_util.is_login_get_username(access_token):
        return templates.TemplateResponse(
            "login.html", {"request": request, "is_login": True}
        )
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/user/login")
async def login(
    username: Optional[str] = Form(...),  # 获取用户名
    password: Optional[str] = Form(...),  # 获取密码
):
    logger.info("发送登入请求")
    # 要求
    limit = """登入失败，用户名或密码错误"""
    if await login_util.login_user(username, password):
        # 添加cookie
        response = RedirectResponse("/index", status_code=302)
        response.set_cookie(
            key="access_token",  # 设置 Cookie 的键
            value=await login_util.get_access_jwt(username),  # 设置 Cookie 的值
            max_age=60 * login_util.login_time_minute,  # 设置 Cookie 的过期时间
        )
        return response
    return {"error": str(limit)}


@router.get("/user/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/user/register")
async def register(
    username: Optional[str] = Form(...),  # 获取用户名
    password: Optional[str] = Form(...),  # 获取密码
    confirm_password: Optional[str] = Form(...),  # 获取确认密码
    nickname: Optional[str] = Form(...),  # 获取昵称
):
    # 要求
    limit = """
    用户名只能包含字母和数字
    用户名长度为2-15
    密码长度为4-15
    昵称长度为2-20
    密码和确认密码必须相同
    """
    logger.info("发送注册请求")
    if await login_util.register_user(username, password, confirm_password, nickname):
        logger.info("注册成功，重定向到登入页面")
        response = RedirectResponse("/user/login", status_code=302)
        # 删除登入的 Cookie
        response.delete_cookie(key="access_token")
        return response
    return {"error": str(limit)}
