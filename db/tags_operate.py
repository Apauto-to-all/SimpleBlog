import asyncio
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


# 标签表操作类
class TagsOperation:
    # 创建标签，首先删除所有标签，再插入新标签
    async def tags_insert(self, tag_list: list, blog_id: int):
        """
        创建标签
        :param tag: 标签列表，包含多个标签
        :param blog_id: 博客id
        :return: 创建成功返回True，创建失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                async with conn.transaction():
                    sql = """
                    DELETE FROM tags WHERE blog_id = $1;
                    """
                    await conn.execute(sql, blog_id)

                    for tag in tag_list:
                        sql = """
                        INSERT INTO tags (tag, blog_id) VALUES ($1, $2);
                        """
                        await conn.execute(sql, tag, blog_id)
                    logger.info(f"博客-{blog_id}插入标签-{tag_list}成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False
        return True

    # 查询一个博客的所有标签，列表形式返回
    async def tags_select(self, blog_id: int):
        """
        查询一个博客的所有标签
        :param blog_id: 博客id
        :return: 查询成功返回标签列表，查询失败返回[]
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT tag FROM tags WHERE blog_id = $1;
                """
                tags = await conn.fetch(sql, blog_id)
                if not tags:
                    logger.info(f"博客-{blog_id}没有标签！")
                    return []
                logger.info(f"博客-{blog_id}查询标签成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []
        return [record.get("tag") for record in tags]

    # 获取标签列表，包含标签和对应的博客数量
    async def tags_select_view(self) -> dict:
        """
        查询标签视图，获取标签列表，包含标签和对应的博客数量
        标签视图按照博客数量降序排列
        :return: 查询成功返回标签列表，查询失败返回{}
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT tag, blog_count
                FROM tag_view;
                """
                tags = await conn.fetch(sql)
                tags_dict = {tag["tag"]: tag["blog_count"] for tag in tags}
                logger.info(f"查询标签视图成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return {}
        return tags_dict if tags_dict else {}

    # 查询某个标签下的所有博客，只保留公开博客
    async def tags_select_blog(self, tag: str, strat: int, count: int):
        """
        查询某个标签下的所有博客，按照发布时间倒序排列，分页查询
        :param tag: 标签
        :param strat: 起始位置
        :param count: 获取博客数量
        :return: 查询成功返回博客列表，查询失败返回[]
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                FROM blogs
                WHERE blog_id IN (SELECT blog_id FROM tags WHERE tag = $1) 
                AND is_public = True
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3;
                """
                blogs_list = await conn.fetch(sql, tag, count, strat)
                logger.info(f"标签-{tag}-查询博客成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []
        return blogs_list if blogs_list else []


"""
标签表：
标签 - 自定义，2-15位
博客id - 外键，关联博客表
二者联合主键
"""
"""
CREATE TABLE IF NOT EXISTS tags (
    tag varchar(15),
    blog_id int REFERENCES blogs(blog_id),
    PRIMARY KEY (tag, blog_id)
);
"""
"""
标签视图：
标签 - 自定义，2-15位
博客数量 - 该标签对应的博客数量
"""
"""
CREATE VIEW tag_view AS
SELECT tag, COUNT(blog_id) AS blog_count
FROM tags
GROUP BY tag
ORDER BY blog_count DESC;
"""
