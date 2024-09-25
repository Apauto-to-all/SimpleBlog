import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class AdminsOperate:

    async def admin_insert(self, username: str, end_time: int):
        """
        插入管理员
        :param username: 用户名
        :param end_time: 管理员持续时间，使用int（time.time()）存储
        :return: 插入成功返回True，插入失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO admins (username, end_time)
                VALUES ($1, $2)
                ON CONFLICT (username) 
                DO UPDATE SET end_time = EXCLUDED.end_time;
                """
                await conn.execute(sql, username, end_time)
                logger.info(f"用户{username}成为管理员成功！结束时间为{end_time}")
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    async def admin_delete(self, username: str):
        """
        删除管理员
        :param username: 用户名
        :return: 删除成功返回True，删除失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                DELETE FROM admins WHERE username = $1;
                """
                await conn.execute(sql, username)
                logger.info(f"用户{username}删除管理员成功！")
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    async def admin_end_time(self, username: str):
        """
        获取管理员持续时间
        :param username: 用户名
        :return: 获取成功返回管理员持续时间，获取失败返回None
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT end_time 
                FROM admins 
                WHERE username = $1;
                """
                end_time = await conn.fetchval(sql, username)
                logger.info(f"用户{username}获取管理员持续时间成功！")
                return end_time if end_time else -1
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return None


# 是否是管理员表
"""
管理员表，在表中的都是管理员：
用户名 - 外键，关联用户表
持续时间 - 管理员持续时间，使用int（time.time()）存储
"""
sql = """
CREATE TABLE IF NOT EXISTS admins (
    username varchar(15) REFERENCES users(username) not null,
    end_time int not null,
    PRIMARY KEY (username)
);
"""
