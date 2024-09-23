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

from utils import blog_util, login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 显示作者信息页面
@router.get("/author/{username}", response_class=HTMLResponse)
async def author(
    request: Request,
    username: Optional[str] = None,
):
    if username:
        # 获取作者信息
        user_dict = await login_util.get_user_dict(username)
        # 去除密码
        if user_dict:
            user_dict.pop("password", None)
            # 返回页面
            return templates.TemplateResponse(
                "author/author.html",
                {"request": request, "user_dict": user_dict},
            )
    # 返回页面
    return templates.TemplateResponse(
        "author/author.html",
        {"request": request, "user_dict": {}},
    )
