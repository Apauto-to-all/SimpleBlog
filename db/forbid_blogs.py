import time
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class ForbidBlogOperation:
    # 禁止博客公开
    async def forbid_blog(self, blog_id: int):
        """
        禁止博客公开
        :param blog_id: 博客id
        :return: 是否成功
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO forbid_blogs (blog_id) 
                VALUES ($1) ON CONFLICT (blog_id) 
                DO NOTHING;
                """
                await conn.execute(sql, blog_id)
                logger.info(f"禁止博客 {blog_id} 公开成功")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 解除禁止博客公开
    async def unforbid_blog(self, blog_id: int):
        """
        解除禁止博客公开
        :param blog_id: 博客id
        :return: 是否成功
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                DELETE FROM forbid_blogs 
                WHERE blog_id = $1;
                """
                await conn.execute(sql, blog_id)
                logger.info(f"解除博客 {blog_id} 公开成功")
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    # 判断博客是否被禁止公开
    async def is_forbid_blog(self, blog_id: int):
        """
        判断博客是否被禁止公开
        :param blog_id: 博客id
        :return: 是否被禁止公开
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT blog_id 
                FROM forbid_blogs 
                WHERE blog_id = $1;
                """
                blog_id = await conn.fetchval(sql, blog_id)
                if blog_id:
                    logger.info(f"博客 {blog_id} 被禁止公开")
                    return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
        return False


# 创建博客禁止公开表
"""
博客禁止公开表：
博客id - 外键，关联博客表
"""
sql = """
CREATE TABLE IF NOT EXISTS forbid_blogs (
    blog_id int REFERENCES blogs(blog_id) not null,
    PRIMARY KEY (blog_id)
);
"""
