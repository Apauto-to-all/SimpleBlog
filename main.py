import importlib
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
from db.connection import DatabaseOperation

# 获取日志记录器
logger = logging.getLogger(__name__)

app = FastAPI()  # 创建 FastAPI 实例

db_operation = DatabaseOperation()  # 创建数据库操作对象


async def startup_event():  # 连接数据库
    await db_operation.connectPool()
    logger.info("连接数据库")


app.add_event_handler("startup", startup_event)  # 注册事件，项目启动时连接数据库


async def shutdown_event():  # 关闭数据库连接池
    await db_operation.pool.close()
    logger.info("关闭数据库连接池")


app.add_event_handler("shutdown", shutdown_event)  # 项目关闭时关闭数据库连接池


app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件目录
app.mount("/layui", StaticFiles(directory="layui"), name="layui")  # layui 静态文件目录


@app.get("/favicon.ico")  # 获取网站图标
async def get_favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")  # 返回网站图标


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/index", status_code=303)


# 路由模块列表
route_modules = [
    "routes.index",
    "routes.admin.admin",
    "routes.admin.blog_admin",
    "routes.admin.check_admin",
    "routes.admin.user_admin",
    "routes.author.author",
    "routes.blog.blog",
    "routes.blog.get_blog",
    "routes.blog.like_blog",
    "routes.blog.search_blog",
    "routes.blog.comment_blog",
    "routes.creation.creation",
    "routes.creation.blog_creation",
    "routes.login.login",
    "routes.login.register",
    "routes.login.post_login",
    "routes.login.post_register",
    "routes.login.get_captcha",
    "routes.tag.tag",
    "routes.tag.search_tag",
    "routes.user.user",
    "routes.user.edit_user",
    "routes.user.get_user",
]
# 动态导入模块并注册路由
for module_name in route_modules:
    module = importlib.import_module(module_name)
    app.include_router(module.router)


if __name__ == "__main__":
    logger.info("启动 FastAPI 服务")

    try:
        uvicorn.run(
            app, host=config.host, port=config.port, log_config=None
        )  # 启动 FastAPI 服务
    except KeyboardInterrupt:
        logger.info("关闭 FastAPI 服务")
