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


# 标签搜索列表
@router.get("/tag/search", response_class=HTMLResponse)
async def tag_search(
    request: Request,
    tag: str = Query(None, description="标签"),
):
    return templates.TemplateResponse(
        "tag_search.html", {"request": request, "tag": tag}
    )


# 获取标签搜索列表
@router.get("/tag_search_list")
async def tag_search_list(
    tag: str = Query(None, description="标签"),
    start: int = Query(0, description="起始位置"),
    count: int = Query(10, description="获取博客数量"),
):
    # 参数校验
    if not tag and not isinstance(start, int) and not isinstance(count, int):
        return JSONResponse(
            content={"success": False, "message": "参数错误"}, status_code=400
        )
    # 分割标签
    tags_list = tag.replace("，", ",").split(",")
    # 获取标签搜索列表
    blog_list = await tag_util.get_tag_search_list(tags_list, start, count)
    return JSONResponse(content=blog_list, status_code=200)
