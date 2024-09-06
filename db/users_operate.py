import sys
import traceback
import asyncpg  # 导入 asyncpg 模块，用于异步访问 PostgreSQL 数据库

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

from connection import DatabaseOperation


# 数据库用户操作类
class UserOperation(DatabaseOperation):
    def __init__(self):
        super().__init__()

    # 用户注册
    async def users_insert(self, username: str, password: str, nickname: str):
        """
        用户注册
        :param username: 用户名
        :param password: 密码
        :param nickname: 昵称
        :return: 注册成功返回True，注册失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO users (username, password, nickname) VALUES ($1, $2, $3);
                """
                await conn.execute(sql, username, password, nickname)
                logger.info(f"用户{username}注册成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True


"""
用户表：
用户名（id）- 主键，用户自定义，使用字母+数字，唯一，2-15位
密码 - 6-15位，包含字母和数字
昵称 - 2-20位，不包含特殊字符
"""
"""
CREATE TABLE IF NOT EXISTS users (
    username varchar(15) NOT NULL,
    password varchar(15) NOT NULL,
    nickname varchar(20) NOT NULL,
    PRIMARY KEY (username)
);
"""
