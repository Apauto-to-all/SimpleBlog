from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
    Query,  # 功能：用于获取查询参数
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from typing import Optional  # 功能：用于声明可选参数

import logging

from utils import blog_util  # 导入博客工具

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/blog", response_class=HTMLResponse)
@router.get("/blog/{blog_id}", response_class=HTMLResponse)
async def blog(
    request: Request,
    blog_id: Optional[int] = None,
):
    if blog_id:
        # 获取博客所有信息
        blog_dict = await blog_util.get_blog_info(blog_id)
        if blog_dict:
            # 博客浏览量加一
            await blog_util.blog_views_add_one(blog_id)
            # 返回页面
            return templates.TemplateResponse(
                "blog.html",
                {"request": request, "blog_dict": blog_dict},
            )
    # 跳转到首页
    return templates.TemplateResponse("blog_404.html", {"request": request})


# 点赞博客
@router.get("/like_blog")
async def like_blog(
    blog_id: int = Query(..., description="博客id"),
):
    # 判断博客id是否为整数，是否为空
    if not blog_id and not isinstance(blog_id, int):
        return JSONResponse(
            content={"success": False, "message": "无效的博客ID"}, status_code=400
        )
    # 博客点赞量加一
    await blog_util.blog_likes_add_one(blog_id)
    return JSONResponse(
        content={"success": True, "message": "点赞成功！"}, status_code=200
    )
