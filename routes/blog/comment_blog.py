from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Cookie,  # 功能：用于操作 Cookie
    Query,  # 功能：用于获取查询参数
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import JSONResponse
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util, login_util, comment_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 发表评论
@router.get("/blog/api/submit_comment")
async def submit_comment(
    blog_id: int = Query(..., description="博客 ID"),
    comment: str = Query(..., description="评论内容"),
    access_token: Optional[str] = Cookie(None),
):
    # 判断博客 ID 是否为整数
    if not isinstance(blog_id, int):
        return JSONResponse(
            content={"success": False, "message": "无效的博客 ID"}, status_code=400
        )
    # 判断评论内容是否为空
    if not comment:
        return JSONResponse(
            content={"success": False, "message": "评论内容不能为空"}, status_code=400
        )
    # 判断用户是否登录
    if not access_token:
        return JSONResponse(
            content={"success": False, "message": "请先登录"}, status_code=401
        )
    username = await login_util.get_user_from_jwt(access_token)
    user_dict = await login_util.get_user_dict(username)
    if not user_dict:
        return JSONResponse(
            content={"success": False, "message": "请先登录"}, status_code=401
        )
    # 发表评论
    result = await comment_util.submit_comment(blog_id, username, comment)
    return JSONResponse(content=result, status_code=200)


# 删除评论
@router.get("/blog/api/delete_comment")
async def delete_comment(
    blog_id: int = Query(..., description="博客 ID"),
    comment_time: int = Query(..., description="评论时间"),
    username: str = Query(..., description="用户名"),
    access_token: Optional[str] = Cookie(None),
):
    # 判断博客 ID 是否为整数
    if not isinstance(blog_id, int):
        return JSONResponse(
            content={"success": False, "message": "无效的博客 ID"}, status_code=400
        )
    # 判断评论时间是否为整数
    if not isinstance(comment_time, int):
        return JSONResponse(
            content={"success": False, "message": "无效的评论时间"}, status_code=400
        )
    # 判断用户是否登录
    if not access_token:
        return JSONResponse(
            content={"success": False, "message": "请先登录"}, status_code=401
        )
    username = await login_util.get_access_jwt(access_token)
    user_dict = await login_util.get_user_dict(username)
    if not user_dict:
        return JSONResponse(
            content={"success": False, "message": "请先登录"}, status_code=401
        )
    # 删除评论
    result = await comment_util.delete_comment(blog_id, username, comment_time)
    return JSONResponse(content=result, status_code=200)


# 获取评论
@router.get("/blog/api/get_comments")
async def get_comments(
    blog_id: int = Query(..., description="博客 ID"),
    start: int = Query(0, description="起始位置"),
    count: int = Query(10, description="获取评论数量"),
):
    # 判断博客 ID 是否为整数
    if not isinstance(blog_id, int):
        return JSONResponse(
            content={"success": False, "message": "无效的博客 ID"}, status_code=400
        )
    # 获取评论
    comments = await comment_util.get_comments(blog_id, start, count)
    [
        {
            "blog_id": 1,  # 博客 ID
            "username": "用户名",  # 用户名
            "nickname": "昵称",  # 昵称
            "content": "评论内容",  # 评论内容
            "comment_time": 1611715200,  # 评论时间
            "comment_time_show": "2021-01-27 00:00:00",  # 评论时间（格式化）
            "avatar_url": "/img/avatar/用户名?t=1611715200",  # 用户头像
        }
    ]
    return JSONResponse(content=comments, status_code=200)
