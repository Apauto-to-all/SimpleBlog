from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Cookie,  # 功能：用于操作 Cookie
    Query,  # 功能：用于获取查询参数
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import JSONResponse
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 获取博客信息列表
@router.get("/blog_list/{blog_type}")
async def blog_list(
    blog_type: Optional[str] = None,
    start: int = Query(0, description="起始位置"),
    count: int = Query(10, description="获取博客数量"),
):
    # 判断博客类型是否有效，判断起始位置和获取博客数量是否为整数
    if (
        not isinstance(start, int)
        and not isinstance(count, int)
        and blog_type not in ["new", "hot", "hot_month", "best"]
    ):
        return JSONResponse(
            content={"success": False, "message": "无效的博客类型"}, status_code=400
        )
    [
        {
            "blog_id": 1,
            "title": "博客标题",
            "content": "博客内容",
            "username": "博客作者",
            "nickname": "博客作者昵称",
            "views": "阅读量",
            "likes": "点赞量",
            "created_at": "发布时间",
            "last_modified": "最后修改时间",
            "tags": ["标签1", "标签2"],
            "is_public": "是否公开",
        },
    ]
    # 获取博客信息列表
    blog_list = await blog_util.get_blogs_list(blog_type, start, count)
    return JSONResponse(content=blog_list, status_code=200)


# 获取用户创作的博客信息列表
@router.get("/user_blog_list/{username}")
async def user_blog_list(
    username: Optional[str] = None,
    start: int = Query(0, description="起始位置"),
    count: int = Query(10, description="获取博客数量"),
    is_all: bool = Query(False, description="是否获取全部博客"),
    access_token: Optional[str] = Cookie(None),
):
    # 判断用户名是否为空，判断起始位置和获取博客数量是否为整数
    if (
        not username
        and not isinstance(start, int)
        and not isinstance(count, int)
        and not isinstance(is_all, bool)
    ):
        return JSONResponse(
            content={"success": False, "message": "无效的用户名"}, status_code=400
        )

    if is_all:  # 需要获取全部博客，判断是否是用户自己
        if access_token and await login_util.is_login(access_token, username):
            is_all = True
        else:  # 如果不是用户自己，不允许获取全部博客
            is_all = False

    # 获取用户创作的博客信息列表，只获取公开博客
    blog_list = await blog_util.get_user_blogs_list(username, start, count, is_all)
    return JSONResponse(content=blog_list, status_code=200)
