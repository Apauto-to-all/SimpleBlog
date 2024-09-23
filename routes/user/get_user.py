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


# API获取用户信息以及跳转链接
@router.get("/user/api/get_info")
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

    return ["未知", "未知用户", "/login"]


# 获取用户头像文件
@router.get("/img/avatar")
@router.get("/img/avatar/{username}")
async def get_user_avatar(
    username: Optional[str] = None,
):
    if username:
        user_dict = await login_util.get_user_dict(username)
        if user_dict:
            avatar_path = user_dict.get("avatar_path")
            # 格式：static/img/avatar/用户名.png
            if avatar_path and os.path.exists(avatar_path):
                return FileResponse(avatar_path)

    return FileResponse("static/img/user_default_avatar.png")
