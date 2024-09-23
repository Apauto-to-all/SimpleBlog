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


# 登录页面
@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    access_token: Optional[str] = Cookie(None),
):
    if access_token and await login_util.is_login(access_token):
        return templates.TemplateResponse(
            "login.html", {"request": request, "is_login": True}
        )
    return templates.TemplateResponse("login.html", {"request": request})


# 注销页面
@router.get("/logout")
async def logout():
    response = RedirectResponse("/index", status_code=302)
    response.delete_cookie(key="access_token")
    return response
