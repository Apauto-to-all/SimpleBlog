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


@router.get("/blog", response_class=HTMLResponse)
@router.get("/blog/{blog_id}", response_class=HTMLResponse)
async def blog(
    request: Request,
    blog_id: Optional[int] = None,
):
    if blog_id:
        # 获取博客所有信息
        blog_dict = await blog_util.get_blog_info(blog_id)
        if blog_dict and blog_dict.get("is_public") == True:
            # 博客浏览量加一
            await blog_util.blog_views_add_one(blog_id)
            # 返回页面
            return templates.TemplateResponse(
                "blog.html",
                {"request": request, "blog_dict": blog_dict},
            )
    # 跳转到首页
    return templates.TemplateResponse("blog_404.html", {"request": request})


# 搜索博客
@router.get("/blog_search", response_class=HTMLResponse)
async def blog_search(
    request: Request,
    keyword: str = Query(None, description="关键字"),
):
    return templates.TemplateResponse(
        "blog_search.html", {"request": request, "keyword": keyword}
    )
