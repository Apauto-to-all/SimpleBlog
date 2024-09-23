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
@router.get("/tag_search", response_class=HTMLResponse)
async def tag_search(
    request: Request,
    tag: str = Query(None, description="标签"),
):
    return templates.TemplateResponse(
        "tag/tag_search.html", {"request": request, "tag": tag}
    )
