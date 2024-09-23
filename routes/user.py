import os
import time
from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import FileResponse, HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util, admin_util

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

    return RedirectResponse("/user_login", status_code=302)


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
        # 判断用户是否被禁言
        user_dict["is_forbid"] = await admin_util.is_forbid_user(user_dict["username"])
        # 禁言结束时间
        user_dict["forbid_end_time"] = (
            await admin_util.get_forbid_end_time(user_dict["username"])
            if user_dict["is_forbid"]
            else -1
        )
        # 禁言剩余时间
        user_dict["forbid_remaining_time"] = (
            user_dict["forbid_end_time"] - int(time.time())
            if user_dict["is_forbid"]
            else -1
        )
        # 如果被禁言，转化为时间格式
        if user_dict["is_forbid"]:
            user_dict["forbid_end_time"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(user_dict["forbid_end_time"])
            )
            user_dict["forbid_remaining_time"] = time.strftime(
                "%H:%M:%S", time.gmtime(user_dict["forbid_remaining_time"])
            )

        return templates.TemplateResponse(
            "user_blog.html",
            {
                "request": request,
                "user_dict": user_dict,
            },
        )

    return RedirectResponse("/user_login", status_code=302)


# API获取用户信息以及跳转链接
@router.get("/user_info")
async def is_login(
    access_token: Optional[str] = Cookie(None),
):
    if access_token:
        username = await login_util.get_user_from_jwt(access_token)
        if username:
            user_dict = await login_util.get_user_dict(username)
            if user_dict:
                return [
                    username,
                    user_dict.get("nickname", "未知用户"),
                    f"/user/{username}",
                ]

    return ["未知", "未知用户", "/user_login"]


# 获取用户头像文件
@router.get("/img/user_avatar/{username}")
async def get_user_avatar(
    username: Optional[str] = None,
):
    if username:
        user_dict = await login_util.get_user_dict(username)
        if user_dict:
            avatar_path = user_dict.get("avatar_path")
            # 格式：static/img/user_avatar/用户名.png
            if avatar_path and os.path.exists(avatar_path):
                return FileResponse(avatar_path)

    return FileResponse("static/img/user_default_avatar.png")
