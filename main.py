from fastapi import FastAPI, Cookie  # 导入 FastAPI 框架
import uvicorn
from fastapi.responses import (
    FileResponse,
    HTMLResponse,  # 用于返回 HTML 响应
    RedirectResponse,  # 用于重定向
)
from fastapi.staticfiles import StaticFiles  # 静态文件目录
import config  # 导入配置文件
from typing import Optional
import logging
from routes import index, blog  # 导入路由模块

# 获取日志记录器
logger = logging.getLogger(__name__)

app = FastAPI()  # 创建 FastAPI 实例
app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录


@app.get("/favicon.ico")  # 获取网站图标
async def get_favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")  # 返回网站图标


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/index", status_code=303)


app.include_router(index.router)  # 注册首页路由
app.include_router(blog.router)  # 注册博客路由

if __name__ == "__main__":
    logger.info("启动 FastAPI 服务")

    try:
        uvicorn.run(
            app, host=config.host, port=config.port, log_config=None
        )  # 启动 FastAPI 服务
    except KeyboardInterrupt:
        logger.info("关闭 FastAPI 服务")
