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


@router.post("/revise_blog/{blog_id}")
async def write_blog(
    access_token: Optional[str] = Cookie(None),
    blog_id: Optional[int] = None,
    markdown_content: Optional[str] = Form(...),
    title: Optional[str] = Form(...),
    tags: Optional[str] = Form(...),
    is_public: Optional[bool] = Form(...),
):
    if access_token:
        username = await login_util.get_user_from_jwt(access_token)
        if username and await login_util.is_login(access_token, username):
            if (
                await admin_util.is_forbid_user(username) and is_public
            ):  # 禁言用户不能修改公开博客
                return RedirectResponse(f"/user/{username}/blog", status_code=302)
            if await admin_util.is_forbid_blog(blog_id):
                # 被禁止公开，只能修改为草稿
                is_public = False
            result = await blog_util.revise_blog(
                blog_id, title, markdown_content, tags, is_public
            )
            if result:
                # if is_public:
                #     return RedirectResponse(f"/blog/{blog_id}", status_code=302)
                return RedirectResponse(f"/user/{username}/blog", status_code=302)
    # 跳转自定义错误页面
    return {"error": "用户验证失败，或者博客修改失败！"}


@router.post("/write_blog")
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
            is_public = (
                False if await admin_util.is_forbid_user(username) else is_public
            )  # 禁言用户不能写公开博客
            blog_id = await blog_util.write_blog(
                username, title, markdown_content, tags, is_public
            )
            if blog_id != -1:
                # if is_public:
                #     return RedirectResponse(f"/blog/{blog_id}", status_code=302)
                return RedirectResponse(f"/user/{username}/blog", status_code=302)
    # 跳转自定义错误页面
    return {"error": "用户验证失败，或者博客写入失败！"}
