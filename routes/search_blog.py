from fastapi import (
    APIRouter,
    Query,  # 功能：用于创建路由
    Request,
    Request,
    Cookie,  # 功能：用于操作 Cookie
)
from fastapi.templating import Jinja2Templates  # 功能：用于渲染模板
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)
from typing import Optional  # 功能：用于声明可选参数
import logging

from utils import blog_util, login_util, tag_util

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 搜索博客
@router.get("/blog_search", response_class=HTMLResponse)
async def blog_search(
    request: Request,
    keyword: str = Query(None, description="关键字"),
):
    return templates.TemplateResponse(
        "blog_search.html", {"request": request, "keyword": keyword}
    )


@router.get("/blog_search_list")
async def blog_search_list(
    keyword: str = Query(None, description="关键字"),
    start: int = Query(0, description="起始位置"),
    count: int = Query(10, description="获取博客数量"),
):
    # 参数校验
    if not keyword and not isinstance(start, int) and not isinstance(count, int):
        return JSONResponse(
            content={"success": False, "message": "参数错误"}, status_code=400
        )
    # 获取博客搜索列表
    blog_list = await blog_util.get_blog_search_list(keyword, start, count)
    return JSONResponse(content=blog_list, status_code=200)
