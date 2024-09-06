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

import logging  # 功能：用于记录日志

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/blog", response_class=HTMLResponse)
@router.get("/blog/{blog_id}", response_class=HTMLResponse)
async def index(request: Request, blog_id: Optional[int] = None):
    if not blog_id:
        # 跳转到首页
        return RedirectResponse("/")
    return templates.TemplateResponse("blog.html", {"request": request})
