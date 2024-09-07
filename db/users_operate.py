import asyncio
import sys
import traceback
import asyncpg  # 导入 asyncpg 模块，用于异步访问 PostgreSQL 数据库

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


# 数据库用户操作类
class UserOperation:
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
                # 查询用户名是否存在
                sql = """
                SELECT * FROM users WHERE username = $1;
                """
                user = await conn.fetchrow(sql, username)
                if user:
                    logger.info(f"用户{username}已存在！取消注册！")
                    return False
                sql = """
                INSERT INTO users (username, password, nickname) VALUES ($1, $2, $3);
                """
                await conn.execute(sql, username, password, nickname)
                logger.info(f"用户{username}注册成功！")
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    # 查询用户，获取密码
    async def users_select_password(self, username: str):
        """
        查询用户，获取密码
        :param username: 用户名
        :return: 返回用户密码，查询失败返回None
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT password FROM users WHERE username = $1;
                """
                password = await conn.fetchval(sql, username)
                logger.info(f"用户{username}查询密码成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return None
        return password

    # 用户名是否存在
    async def users_select_username(self, username: str):
        """
        查询用户
        :param username: 用户名
        :return: 返回用户信息，查询失败返回None
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT * FROM users WHERE username = $1;
                """
                user = await conn.fetchrow(sql, username)
                logger.info(f"用户{username}查询成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return None
        return user


"""
用户表：
用户名（id）- 主键，用户自定义，使用字母+数字，唯一，2-15位
密码 - 4-15位，包含字母和数字
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
