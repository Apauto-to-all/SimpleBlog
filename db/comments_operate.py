import time
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class CommentsOperate:
    async def comments_insert(self, blog_id: int, username: str, content: str):
        """
        插入评论
        :param blog_id: 博客id
        :param username: 用户名
        :param content: 评论内容
        :return: 插入成功返回True，插入失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO comments (blog_id, username, content, comment_time) VALUES ($1, $2, $3, $4);
                """
                await conn.execute(sql, blog_id, username, content, int(time.time()))
                logger.info(f"用户{username}评论博客-{blog_id}成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 删除评论
    async def comments_delete(self, blog_id: int, username: str, comment_time: int):
        """
        删除评论
        :param blog_id: 博客id
        :param username: 用户名
        :param comment_time: 评论时间
        :return: 删除成功返回True，删除失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                DELETE FROM comments WHERE blog_id = $1 AND username = $2 AND comment_time = $3;
                """
                await conn.execute(sql, blog_id, username, comment_time)
                logger.info(f"用户{username}删除博客-{blog_id}评论成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 获取评论
    async def comments_get(self, blog_id: int, start: int, count: int):
        """
        获取评论
        :param blog_id: 博客id
        :param start: 起始位置
        :param count: 获取数量
        :return: 获取成功返回评论列表，获取失败返回None
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT blog_id, username, content, comment_time
                FROM comments
                WHERE blog_id = $1
                ORDER BY comment_time DESC
                LIMIT $2 OFFSET $3;
                """
                comments = await conn.fetch(sql, blog_id, count, start)
                logger.info(f"获取博客-{blog_id}评论成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return None
        return comments


# 创建博客评论表
"""
博客评论表：
博客id - 外键，关联博客表
用户名 - 外键，关联用户表
评论内容 - 无限制
评论时间 - 使用时间戳存储，int（time.time()）格式
主键 - 博客id + 用户名 + 评论时间
"""
sql = """
CREATE TABLE IF NOT EXISTS comments (
    blog_id int REFERENCES blogs(blog_id) not null,
    username varchar(15) REFERENCES users(username) not null,
    content text,
    comment_time int,
    PRIMARY KEY (blog_id, username, comment_time)
);
"""
