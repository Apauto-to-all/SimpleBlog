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

from utils import blog_util, login_util, admin_util, check_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 获取用户需要审核的博客
@router.get("/admin/api/get_user_blogs_need_check", response_class=JSONResponse)
async def get_user_blogs(
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
    blogs_list = await check_util.get_need_check_blogs(start=start, count=limit)
    blogs_count = await check_util.get_need_check_blogs_count()
    return JSONResponse(
        content={"code": 0, "msg": "", "count": blogs_count, "data": blogs_list},
        status_code=200,
    )


# 获取已经审核的博客
@router.get("/admin/api/get_user_blogs_checked", response_class=JSONResponse)
async def get_user_blogs_checked(
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
    blogs_list = await check_util.get_checked_blogs(
        start=start, count=limit, is_all=True
    )
    blogs_count = await check_util.get_checked_blogs_count()
    return JSONResponse(
        content={"code": 0, "msg": "", "count": blogs_count, "data": blogs_list},
        status_code=200,
    )


# 审核博客
@router.get("/admin/api/check_blog", response_class=JSONResponse)
async def check_blog(
    access_token: Optional[str] = Cookie(None),
    blog_id: int = Query(None),
    is_pass: bool = Query(None),
):
    if not access_token or not blog_id or is_pass is None:
        username_use = await login_util.get_user_from_jwt(access_token)
        if not (
            username_use
            and await login_util.is_login(access_token, username_use)
            and await admin_util.is_admin(username_use)
        ):
            return JSONResponse(content={"error": "参数错误"}, status_code=400)

    username_use = await login_util.get_user_from_jwt(access_token)
    result = await check_util.pass_check_blog(blog_id, username_use, is_pass)
    return (
        JSONResponse(content={"status": "success"}, status_code=200)
        if result
        else JSONResponse(content={"status": "fail"}, status_code=400)
    )
