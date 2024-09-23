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


# 获取用户的所有博客信息
@router.get("/admin/api/get_user_blogs", response_class=JSONResponse)
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


# 禁止博客公开
@router.get("/admin/api/forbid_blog", response_class=JSONResponse)
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
@router.get("/admin/api/unforbid_blog", response_class=JSONResponse)
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
