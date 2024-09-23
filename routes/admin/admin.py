from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Cookie,  # 功能：用于操作 Cookie
    Query,  # 功能：用于获取查询参数
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util, admin_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 管理员页面
@router.get("/admin", response_class=HTMLResponse)
async def admin(
    request: Request,
    access_token: Optional[str] = Cookie(None),
):
    if access_token and await login_util.is_login(access_token, "admin"):
        return templates.TemplateResponse("admin.html", {"request": request})
    return RedirectResponse("/login", status_code=302)


# 管理用户博客页面
@router.get("/admin/{username}/blog", response_class=HTMLResponse)
async def admin_user_blog(
    request: Request,
    username: Optional[str],
    access_token: Optional[str] = Cookie(None),
):
    if access_token and await login_util.is_login(access_token, "admin"):
        return templates.TemplateResponse(
            "admin_user_blog.html", {"request": request, "username": username}
        )
    return RedirectResponse("/login", status_code=302)
