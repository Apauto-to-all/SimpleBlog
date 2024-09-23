from fastapi import (
    APIRouter,
    Form,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util, admin_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/creation/write/{username}/blog", response_class=HTMLResponse)
async def write_blog(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
):
    user_dict = await login_util.get_user_dict(username)
    if user_dict and access_token and await login_util.is_login(access_token, username):
        return templates.TemplateResponse(
            "creation/write_blog.html", {"request": request}
        )

    return RedirectResponse(f"/user/{username}/blog", status_code=302)


@router.get("/creation/revise/{username}/blog/{blog_id}", response_class=HTMLResponse)
async def write_blog(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
    blog_id: Optional[int] = None,
):
    user_dict = await login_util.get_user_dict(username)
    if (
        user_dict
        and access_token
        and await login_util.is_login(access_token, username)
        and blog_id
    ):
        # 获取博客所有信息
        blog_dict = await blog_util.get_blog_info(blog_id)
        if blog_dict:
            blog_dict["tags_str"] = ",".join(blog_dict["tags"])
            return templates.TemplateResponse(
                "creation/revise_blog.html",
                {"request": request, "blog_dict": blog_dict},
            )
    return RedirectResponse(f"/user/{username}/blog", status_code=302)
