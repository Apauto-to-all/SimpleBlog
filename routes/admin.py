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
    return RedirectResponse("/user_login", status_code=302)


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
    return RedirectResponse("/user_login", status_code=302)


# 获取所有用户信息
@router.get("/admin/get_users", response_class=JSONResponse)
async def get_users(
    access_token: Optional[str] = Cookie(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    if not access_token and not await login_util.is_login(access_token, "admin"):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)
    start = (page - 1) * limit
    users_list = await admin_util.get_all_users(start=start, count=limit)
    all_users_count = await admin_util.get_all_users_count()
    return JSONResponse(
        content={"code": 0, "msg": "", "count": all_users_count, "data": users_list},
        status_code=200,
    )


# 获取用户的所有博客信息
@router.get("/admin/get_user_blogs", response_class=JSONResponse)
async def get_user_blogs(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    if (
        not access_token
        or not username
        or not await login_util.is_login(access_token, "admin")
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    start = (page - 1) * limit
    blogs_list = await blog_util.get_user_blogs_list(
        username=username, start=start, count=limit, is_all=True
    )
    all_blogs_count = await blog_util.get_user_blogs_count(username)
    return JSONResponse(
        content={"code": 0, "msg": "", "count": all_blogs_count, "data": blogs_list},
        status_code=200,
    )


# 禁言用户
@router.get("/admin/forbid_user", response_class=JSONResponse)
async def forbid_user(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),
    minutes: int = Query(0),  # 默认禁言 0 分钟
):
    if (
        not access_token
        and not username
        and not isinstance(minutes, int)
        and minutes < 0
        and not await login_util.is_login(access_token, "admin")
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    result = await admin_util.forbid_user(username, minutes)
    return (
        JSONResponse(content={"status": "success"}, status_code=200)
        if result
        else JSONResponse(content={"status": "fail"}, status_code=400)
    )


# 解除禁言
@router.get("/admin/unforbid_user", response_class=JSONResponse)
async def unforbid_user(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),
):
    if (
        not access_token
        and not username
        and not await login_util.is_login(access_token, "admin")
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    result = await admin_util.unforbid_user(username)
    return (
        JSONResponse(content={"status": "success"}, status_code=200)
        if result
        else JSONResponse(content={"status": "fail"}, status_code=400)
    )


# 禁止博客公开
@router.get("/admin/forbid_blog", response_class=JSONResponse)
async def forbid_blog(
    access_token: Optional[str] = Cookie(None),
    blog_id: int = Query(None),
):
    if (
        not access_token
        and not blog_id
        and not await login_util.is_login(access_token, "admin")
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    result = await admin_util.forbid_blog(blog_id)
    return (
        JSONResponse(content={"status": "success"}, status_code=200)
        if result
        else JSONResponse(content={"status": "fail"}, status_code=400)
    )


# 解除博客禁止公开
@router.get("/admin/unforbid_blog", response_class=JSONResponse)
async def unforbid_blog(
    access_token: Optional[str] = Cookie(None),
    blog_id: int = Query(None),
):
    if (
        not access_token
        and not blog_id
        and not await login_util.is_login(access_token, "admin")
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    result = await admin_util.unforbid_blog(blog_id)
    return (
        JSONResponse(content={"status": "success"}, status_code=200)
        if result
        else JSONResponse(content={"status": "fail"}, status_code=400)
    )
