import os
import time
from PIL import Image
from fastapi import (
    APIRouter,
    File,
    Form,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,
    UploadFile,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
)  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util, admin_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 更新用户信息
@router.post("/user/api/edit")
async def edit_user(
    nickname: Optional[str] = Form(""),  # 获取昵称
    password: Optional[str] = Form(""),  # 获取密码
    confirm_password: Optional[str] = Form(""),  # 获取确认密码
    avatar: UploadFile = File(...),  # 获取头像文件
    access_token: Optional[str] = Cookie(None),  # 获取 access_token
):
    if not (access_token and nickname and password and confirm_password):
        return JSONResponse(content={"message": "参数不能为空"}, status_code=400)

    username = await login_util.get_user_from_jwt(access_token)
    user_dict = await login_util.get_user_dict(username)
    if not user_dict:
        return JSONResponse(content={"message": "用户不存在"}, status_code=404)
    if password != confirm_password:
        return JSONResponse(content={"message": "两次密码不一致"}, status_code=400)
    if not (4 <= len(password) <= 15):
        return JSONResponse(content={"message": "密码长度不符合要求"}, status_code=400)
    if not (2 <= len(nickname) <= 20):
        return JSONResponse(content={"message": "昵称长度不符合要求"}, status_code=400)

    hashed_password = await login_util.encrypt_password(password)
    avatar_path = os.path.join("static", "img", "user_avatar", f"{username}.png")

    # 如果文件夹不存在，创建文件夹
    if not os.path.exists(os.path.dirname(avatar_path)):
        os.makedirs(os.path.dirname(avatar_path))

    try:
        # 保存头像并调整大小
        image = Image.open(avatar.file)
        width_percent = 100 / float(image.size[0])
        height_size = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((100, height_size), Image.LANCZOS)
        image.save(avatar_path)
    except Exception as e:
        pass

    await login_util.update_user(username, nickname, hashed_password, avatar_path)

    return JSONResponse(content={"message": "更新成功", "code": 200}, status_code=200)
