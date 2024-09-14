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
from routes import index, blog, login_register, write_blog, user, get_blog, author, tag

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
    return FileResponse(
        "/static/favicon.ico", media_type="image/x-icon"
    )  # 返回网站图标


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/index", status_code=303)


app.include_router(index.router)  # 注册首页路由
app.include_router(blog.router)  # 注册博客路由
app.include_router(login_register.router)  # 注册登录注册路由
app.include_router(write_blog.router)  # 注册写博客路由
app.include_router(user.router)  # 注册用户路由
app.include_router(get_blog.router)  # 注册获取博客路由
app.include_router(author.router)  # 注册作者路由
app.include_router(tag.router)  # 注册标签路由

if __name__ == "__main__":
    logger.info("启动 FastAPI 服务")

    try:
        uvicorn.run(
            app, host=config.host, port=config.port, log_config=None
        )  # 启动 FastAPI 服务
    except KeyboardInterrupt:
        logger.info("关闭 FastAPI 服务")
