from fastapi import (
    APIRouter,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import HTMLResponse  # 功能：用于返回 HTML 响应
from fastapi.responses import RedirectResponse  # 功能：用于重定向
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
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
