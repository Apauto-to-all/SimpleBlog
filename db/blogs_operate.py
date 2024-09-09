import asyncio
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


# 博客表操作类
class BlogOperation:
    # 创建草稿博客
    async def blogs_insert_draft(self, title: str, content: str, username: str):
        """
        创建草稿博客
        :param title: 博客标题
        :param content: 博客内容
        :param username: 用户名
        :return: 创建成功返回博客id，失败返回None
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                INSERT INTO blogs (title, content, username) VALUES ($1, $2, $3) RETURNING blog_id;
                """
                blog_id = await conn.fetchval(sql, title, content, username)
                logger.info(f"用户{username}创建草稿博客-{blog_id}-{title}成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return None
        return blog_id

    # 设置博客公开，并更新发布时间
    async def blogs_set_public(self, blog_id: int):
        """
        设置博客公开
        :param blog_id: 博客id
        :return: 设置成功返回True，设置失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                UPDATE blogs SET is_public = true , created_at = CURRENT_TIMESTAMP WHERE blog_id = $1;
                """
                await conn.execute(sql, blog_id)
                logger.info(f"博客-{blog_id}设置公开成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 更新博客内容，标题，当前时间
    async def blogs_update(self, blog_id: int, title: str, content: str):
        """
        更新博客内容，标题
        :param blog_id: 博客id
        :param title: 博客标题
        :param content: 博客内容
        :return: 更新成功返回True，更新失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                UPDATE blogs SET title = $1, content = $2, created_at = CURRENT_TIMESTAMP WHERE blog_id = $3;
                """
                await conn.execute(sql, title, content, blog_id)
                logger.info(f"博客-{blog_id}更新成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 读取博客内容，标题，作者，阅读量，点赞量，发布时间，如果不公开返回None
    async def blogs_select(self, blog_id: int):
        """
        读取博客内容，标题，作者，阅读量，点赞量，发布时间
        :param blog_id: 博客id
        :return: 返回博客信息，如果博客不公开返回{}
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT title, content, username, views, likes, created_at 
                FROM blogs 
                WHERE blog_id = $1 AND is_public = true;
                """
                blog_info = await conn.fetchrow(sql, blog_id)
                if not blog_info:
                    logger.info(f"博客-{blog_id}读取失败！")
                    return {}
                blog_dict = {
                    "blog_id": blog_id,  # 博客id
                    "title": blog_info.get("title"),  # 博客标题
                    "content": blog_info.get("content"),  # 博客内容
                    "username": blog_info.get("username"),  # 博客作者
                    "views": blog_info.get("views"),  # 阅读量
                    "likes": blog_info.get("likes"),  # 点赞量
                    "created_at": blog_info.get("created_at"),  # 发布时间
                }
                logger.info(f"博客-{blog_id}读取成功，已经返回内容！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return {}
        return blog_dict if blog_dict else {}


"""
博客表：
博客id - 主键，自增
博客标题 - 2-50位
博客内容 - 无限制
博客作者 - 外键，关联用户表
阅读量 - 默认为0
点赞量 - 默认为0
发布时间 - 默认为当前时间
是否公开 - 默认为不公开，false
"""
"""
CREATE TABLE IF NOT EXISTS blogs (
    blog_id serial,
    title varchar(50) NOT NULL,
    content text,
    username varchar(15) REFERENCES users(username) not null,
    views int DEFAULT 0,
    likes int DEFAULT 0,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    is_public boolean DEFAULT false,
    PRIMARY KEY (blog_id)
);
"""
