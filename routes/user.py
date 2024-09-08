from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/user/{username}", response_class=HTMLResponse)
async def user(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
):
    user_dict = await login_util.get_user_dict(username)
    if user_dict and access_token and await login_util.is_login(access_token, username):
        # 去除密码
        user_dict.pop("password", None)
        return templates.TemplateResponse(
            "user.html",
            {
                "request": request,
                "user_dict": user_dict,
            },
        )

    return RedirectResponse("/index", status_code=302)


@router.get("/user/{username}/blog", response_class=HTMLResponse)
async def user_blog(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
):
    user_dict = await login_util.get_user_dict(username)
    if user_dict and access_token and await login_util.is_login(access_token, username):
        # 去除密码
        user_dict.pop("password", None)
        return templates.TemplateResponse(
            "user_blog.html",
            {
                "request": request,
                "user_dict": user_dict,
            },
        )

    return RedirectResponse("/index", status_code=302)
