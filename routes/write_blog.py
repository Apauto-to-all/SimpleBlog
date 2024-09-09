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

from utils import blog_util, login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/user/{username}/blog/write", response_class=HTMLResponse)
async def write_blog(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
):
    user_dict = await login_util.get_user_dict(username)
    if user_dict and access_token and await login_util.is_login(access_token, username):
        return templates.TemplateResponse("write_blog.html", {"request": request})

    return RedirectResponse("/index", status_code=302)


@router.get("/user/{username}/blog/revise/{blog_id}", response_class=HTMLResponse)
async def write_blog(
    request: Request,
    username: Optional[str] = None,
    access_token: Optional[str] = Cookie(None),
    blog_id: Optional[int] = None,
):
    user_dict = await login_util.get_user_dict(username)
    if user_dict and access_token and await login_util.is_login(access_token, username):
        return templates.TemplateResponse("write_blog.html", {"request": request})

    return RedirectResponse("/index", status_code=302)


@router.post("/user/write_blog")
async def write_blog(
    access_token: Optional[str] = Cookie(None),
    markdown_content: Optional[str] = Form(...),
    title: Optional[str] = Form(...),
    tags: Optional[str] = Form(...),
    is_public: Optional[bool] = Form(...),
):
    if access_token:
        username = await login_util.get_user_from_jwt(access_token)
        if username and await login_util.is_login(access_token, username):
            blog_id = await blog_util.write_blog(
                username, title, markdown_content, tags, is_public
            )
            if blog_id != -1:
                return RedirectResponse(f"/blog/{blog_id}", status_code=302)
    # 跳转自定义错误页面
    return {"error": "用户验证失败，或者博客写入失败！"}
