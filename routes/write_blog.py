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


@router.get("/user/{username}/blog/write", response_class=HTMLResponse)
async def write_blog(request: Request, username: Optional[str] = None):
    return templates.TemplateResponse("write_blog.html", {"request": request})


@router.get("/user/{username}/blog/revise/{blog_id}", response_class=HTMLResponse)
async def write_blog(
    request: Request, username: Optional[str] = None, blog_id: Optional[int] = None
):
    return templates.TemplateResponse("write_blog.html", {"request": request})


@router.post("/user/{username}/write_blog")
async def write_blog(request: Request, username: Optional[str] = None):
    form = await request.form()
    title = form.get("title")
    content = form.get("content")
    blog_id = await blog_util.write_blog(username, title, content)
    return RedirectResponse(f"/blog/{blog_id}")
