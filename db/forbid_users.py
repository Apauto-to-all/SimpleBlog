import time
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class ForbidUserOperation:
    # 禁言用户
    async def forbid_user(self, username: str, end_time: int):
        """
        禁言用户
        :param username: 用户名
        :param end_time: 禁言结束时间
        :return: 是否成功
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO forbid_users (username, end_time) 
                VALUES ($1, $2) ON CONFLICT (username) 
                DO UPDATE SET end_time = $2;
                """
                await conn.execute(sql, username, end_time)
                logger.info(f"禁言用户 {username} 成功")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 判断用户是否被禁言
    async def is_forbid_user(self, username: str):
        """
        判断用户是否被禁言
        :param username: 用户名
        :return: 是否被禁言
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT end_time 
                FROM forbid_users 
                WHERE username = $1;
                """
                end_time = await conn.fetchval(sql, username)
                if end_time and end_time > int(time.time()):
                    logger.info(f"用户 {username} 被禁言")
                    return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
        return False

    # 获取用户禁言结束时间
    async def get_forbid_end_time(self, username: str):
        """
        获取用户禁言结束时间
        :param username: 用户名
        :return: 禁言结束时间
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT end_time 
                FROM forbid_users 
                WHERE username = $1;
                """
                end_time = await conn.fetchval(sql, username)
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
        return end_time if end_time else -1

    # 解除用户禁言
    async def unforbid_user(self, username: str):
        """
        解除用户禁言
        :param username: 用户名
        :return: 是否成功
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                DELETE FROM forbid_users 
                WHERE username = $1;
                """
                await conn.execute(sql, username)
                logger.info(f"解除用户 {username} 禁言成功")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True


# 创建用户禁言表
"""
用户禁言表：
用户名 - 外键，关联用户表
结束时间 - 禁言结束时间，使用int（time.time()）存储
"""
sql = """
CREATE TABLE IF NOT EXISTS forbid_users (
    username varchar(15) REFERENCES users(username) not null,
    end_time int not null,
    PRIMARY KEY (username)
);
"""
