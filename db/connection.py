import sys
import traceback
import asyncpg  # 导入 asyncpg 模块，用于异步访问 PostgreSQL 数据库
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

from private_settings import (
    pgsql_host,
    pgsql_user,
    pgsql_password,
    database_name,
    pgsql_port,
)

from .blogs_operate import BlogOperation
from .tags_operate import TagsOperation
from .users_operate import UserOperation
from .get_blogs import GetBlogs
from .forbid_users import ForbidUserOperation
from .forbid_blogs import ForbidBlogOperation
from .admins_operate import AdminsOperate
from .need_check_blogs import NeedCheckBlogs
from .comments_operate import CommentsOperate


# 数据库操作类
class DatabaseOperation(
    BlogOperation,
    TagsOperation,
    UserOperation,
    GetBlogs,
    ForbidUserOperation,
    ForbidBlogOperation,
    AdminsOperate,
    NeedCheckBlogs,
    CommentsOperate,
):
    _instance = None  # 单例模式
    error_mun = 0  # 错误次数

    def __init__(self):
        if not hasattr(self, "pool"):
            self.pool = None  # 数据库连接池

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseOperation, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # 使用操作用户连接数据库，主要用于查询，更新，插入操作
    async def connectPool(self):
        """
        连接数据库，使用操作用户
        """
        try:
            self.pool = (
                await asyncpg.create_pool(  # 创建数据库连接池，可以异步访问数据库
                    user=pgsql_user,  # 数据库操作用户
                    password=pgsql_password,  # 数据库操作用户密码
                    database=database_name,  # 数据库名称
                    host=pgsql_host,  # 数据库主机
                    port=pgsql_port,  # 数据库端口
                )
            )
            logger.info("数据库连接成功！")
        except Exception as e:
            self.error_mun += 1
            error_info = traceback.format_exc()
            logger.error(error_info)
            logger.error(e)
            if self.error_mun <= 3:
                await self.connectPool()  # 如果连接数据库失败，就重新连接
            else:
                logger.error("数据库连接失败，程序退出")
                sys.exit()

    # 关闭数据库连接
    async def close(self):
        """
        关闭数据库连接
        """
        if self.pool:
            try:
                await self.pool.close()
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                pass
