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

    # 查询用户的所有信息，返回用户信息
    async def users_select(self, username: str) -> dict:
        """
        查询用户
        :param username: 用户名
        :return: 返回用户信息，查询失败返回{}
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT * FROM users WHERE username = $1;
                """
                user = await conn.fetchrow(sql, username)
                if not user:
                    logger.info(f"用户{username}的信息查询失败！")
                    return {}
                user_dict = {
                    "username": user.get("username", None),
                    "password": user.get("password", None),
                    "nickname": user.get("nickname", None),
                    "avatar_path": user.get("avatar_path", None),
                }
                logger.info(f"用户{username}的信息查询成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return {}

            return user_dict if user_dict else {}

    # 查询所有用户信息，返回用户信息列表
    async def users_select_all(self, start: int = 0, count: int = 10) -> list:
        """
        查询所有用户信息
        :param start: 起始位置
        :param count: 获取用户数量
        :return: 用户信息列表
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT username, password, nickname
                FROM users
                ORDER BY username ASC
                LIMIT $1 OFFSET $2;
                """
                users = await conn.fetch(sql, count, start)
                users_list = []
                for user in users:
                    user_dict = {
                        "username": user.get("username", None),
                        "password": user.get("password", None),
                        "nickname": user.get("nickname", None),
                    }
                    users_list.append(user_dict)
                logger.info("管理员查询部分用户信息成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []

            return users_list if users_list else []

    # 查询用户数量
    async def users_count(self) -> int:
        """
        查询用户数量
        :return: 用户数量
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT COUNT(*) FROM users;
                """
                count = await conn.fetchval(sql)
                logger.info("查询用户数量成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return 0

            return count if count else 0

    # 更新用户信息
    async def users_update(
        self, username: str, password: str, nickname: str, avatar_path: str
    ) -> bool:
        """
        更新用户信息
        :param username: 用户名
        :param password: 密码
        :param nickname: 昵称
        :param avatar_path: 头像路径
        :return: 更新成功返回True，更新失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                UPDATE users 
                SET password = $1, nickname = $2, avatar_path = $3 
                WHERE username = $4;
                """
                await conn.execute(sql, password, nickname, avatar_path, username)
                logger.info(f"用户{username}信息更新成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

            return True


# 创建一个用户表
"""
用户表：
用户名（id）- 主键，用户自定义，使用字母+数字，唯一，2-15位
密码 - 4-15位，包含字母和数字，加密后60位
昵称 - 2-20位，不包含特殊字符
头像路径 - 用户头像的路径，可以为空
"""
sql = """
CREATE TABLE IF NOT EXISTS users (
    username varchar(15) NOT NULL,
    password varchar(60) NOT NULL,
    nickname varchar(20) NOT NULL,
    avatar_path text,
    PRIMARY KEY (username)
);
"""
