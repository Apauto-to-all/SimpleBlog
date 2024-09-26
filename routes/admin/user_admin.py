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


# 获取所有用户信息
@router.get("/admin/api/get_users", response_class=JSONResponse)
async def get_users(
    access_token: Optional[str] = Cookie(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    if not access_token:
        username_use = await login_util.get_user_from_jwt(access_token)
        if not (
            username_use
            and await login_util.is_login(access_token, username_use)
            and await admin_util.is_admin(username_use)
        ):
            return JSONResponse(content={"error": "参数错误"}, status_code=400)
    start = (page - 1) * limit
    users_list = await admin_util.get_all_users(start=start, count=limit)
    all_users_count = await admin_util.get_all_users_count()
    return JSONResponse(
        content={"code": 0, "msg": "", "count": all_users_count, "data": users_list},
        status_code=200,
    )


# 禁言用户
@router.get("/admin/api/forbid_user", response_class=JSONResponse)
async def forbid_user(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),
    minutes: int = Query(0),  # 默认禁言 0 分钟
):
    if (
        not access_token
        or not username
        or not isinstance(minutes, int)
        or not minutes < 0
    ):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    username_use = await login_util.get_user_from_jwt(access_token)
    if (
        username_use
        and await login_util.is_login(access_token, username_use)
        and await admin_util.is_admin(username_use)
    ):
        # 如果用户不是超级管理员，不能禁言其他管理员
        if await admin_util.is_admin(username) and username_use != "admin":
            return JSONResponse(content={"status": "fail"}, status_code=400)

        result = await admin_util.forbid_user(username, minutes)
        if result:
            return JSONResponse(content={"status": "success"}, status_code=200)

    return JSONResponse(content={"status": "fail"}, status_code=400)


# 解除禁言
@router.get("/admin/api/unforbid_user", response_class=JSONResponse)
async def unforbid_user(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),
):
    if not access_token or not username:
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    username_use = await login_util.get_user_from_jwt(access_token)
    if (
        username_use
        and await login_util.is_login(access_token, username_use)
        and await admin_util.is_admin(username_use)
    ):
        # 如果用户不是超级管理员，不能解除其他管理员的禁言
        if await admin_util.is_admin(username) and username_use != "admin":
            return JSONResponse(content={"status": "fail"}, status_code=400)

        result = await admin_util.unforbid_user(username)
        if result:
            return JSONResponse(content={"status": "success"}, status_code=200)

    return JSONResponse(content={"status": "fail"}, status_code=400)


# 为用户添加管路权限
@router.get("/admin/api/add_admin", response_class=JSONResponse)
async def add_admin(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),  # 用户名
    days: int = Query(None),  # 管理员权限天数
):
    if not access_token or not username or not days or not isinstance(days, int):
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    username_use = await login_util.get_user_from_jwt(access_token)
    if username_use == "admin":
        result = await admin_util.add_admin(username, days)
        if result:
            return JSONResponse(content={"status": "success"}, status_code=200)

    return JSONResponse(content={"status": "fail"}, status_code=400)


# 删除用户的管理员权限
@router.get("/admin/api/delete_admin", response_class=JSONResponse)
async def delete_admin(
    access_token: Optional[str] = Cookie(None),
    username: str = Query(None),  # 用户名
):
    if access_token and username:
        return JSONResponse(content={"error": "参数错误"}, status_code=400)

    username_use = await login_util.get_user_from_jwt(access_token)
    if username_use == "admin":
        result = await admin_util.delete_admin(username)
        if result:
            return JSONResponse(content={"status": "success"}, status_code=200)

    return JSONResponse(content={"status": "fail"}, status_code=400)
