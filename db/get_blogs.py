import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


# 获取博客信息操作类
class GetBlogs:
    # 获取最新博客信息
    async def blogs_select_list(self, blog_type: str, start: int, count: int) -> list:
        """
        获取博客信息
        :param blog_type: 博客类型 ('new', 'hot', 'hot_month', 'best')
        :param start: 起始位置
        :param count: 获取博客数量
        :param username: 用户名，默认为 None
        :return: 返回博客信息列表
        """
        """
        new: 最新博客, 
        hot: 热门博客 (一周热门博客, 阅读量 + 点赞量 * 9), 
        hot_month: 一个月热门博客（一个月内热门博客, 阅读量 + 点赞量 * 9）,
        best: 最佳博客 (阅读量 + 点赞量 * 9)
        """
        async with self.pool.acquire() as conn:
            try:
                if blog_type == "new":
                    sql = """
                    SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                    FROM blogs 
                    WHERE is_public = true
                    ORDER BY created_at DESC
                    LIMIT $1 OFFSET $2;
                    """
                elif blog_type == "hot":
                    sql = """
                    SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                    FROM blogs
                    WHERE is_public = true
                    ORDER BY 
                        CASE 
                            WHEN created_at > CURRENT_TIMESTAMP - interval '1 week' THEN 1
                            ELSE 2
                        END,
                        (views + likes * 9) DESC
                    LIMIT $1 OFFSET $2;
                    """
                elif blog_type == "hot_month":
                    sql = """
                    SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                    FROM blogs
                    WHERE is_public = true
                    ORDER BY 
                        CASE 
                            WHEN created_at > CURRENT_TIMESTAMP - interval '1 month' THEN 1
                            ELSE 2
                        END,
                        (views + likes * 9) DESC
                    LIMIT $1 OFFSET $2;
                    """
                elif blog_type == "best":
                    sql = """
                    SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                    FROM blogs
                    WHERE is_public = true
                    ORDER BY (views + likes * 9) DESC
                    LIMIT $1 OFFSET $2;
                    """
                else:
                    return []
                blog_list = await conn.fetch(sql, count, start)
                logger.info(f"获取{blog_type}博客信息成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []
        return blog_list if blog_list else []

    # 获取用户创作的博客信息
    async def blogs_select_list_by_username(
        self,
        username: str,
        start: int = 0,
        count: int = 10,
        is_all: bool = False,
        get_all: bool = False,
    ) -> list:
        """
        获取用户创作的博客信息，按发布时间倒序排列
        :param username: 用户名
        :param start: 起始位置
        :param count: 获取博客数量
        :param is_all: 是否获取全部博客，只有用户自己可以获取全部博客，默认为False
        :param get_all: 是否获取所有博客，无论是否公开，默认为False——管理员使用
        :return: 返回博客信息列表
        """
        async with self.pool.acquire() as conn:
            try:
                if get_all:  # 获取所有博客，无论是否公开，管理员使用
                    sql = """
                    SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                    FROM blogs
                    WHERE username = $1
                    ORDER BY created_at DESC
                    """
                    blog_list = await conn.fetch(sql, username)
                else:
                    if is_all:  # 提供所有博客，无论是否公开
                        sql = """
                        SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                        FROM blogs
                        WHERE username = $1
                        ORDER BY created_at DESC
                        LIMIT $2 OFFSET $3;
                        """
                    else:  # 提供公开博客
                        sql = """
                        SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                        FROM blogs
                        WHERE username = $1
                        AND is_public = true
                        ORDER BY created_at DESC
                        LIMIT $2 OFFSET $3;
                        """
                    blog_list = await conn.fetch(sql, username, count, start)
                logger.info(f"获取{username}的博客信息成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []
        return blog_list if blog_list else []

    # 关键字搜索博客
    async def blogs_search(self, keyword: str, start: int, count: int):
        """
        关键字搜索博客
        :param keyword: 关键字
        :param start: 起始位置
        :param count: 获取博客数量
        :return: 返回博客信息列表
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT blog_id, title, content, username, views, likes, created_at, last_modified, is_public
                FROM blogs
                WHERE is_public = true
                AND (title LIKE '%' || $1 || '%' OR content LIKE '%' || $1 || '%')
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3;
                """
                blog_list = await conn.fetch(sql, keyword, count, start)
                logger.info(f"关键字搜索博客成功！")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []
        return blog_list if blog_list else []


"""
博客表：
博客id - 主键，自增
博客标题 - 2-50位
博客内容 - 无限制
博客作者 - 外键，关联用户表
阅读量 - 默认为0
点赞量 - 默认为0
发布时间 - 默认为当前时间
最后修改时间 - 默认为当前时间
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
    last_modified timestamp DEFAULT CURRENT_TIMESTAMP,
    is_public boolean DEFAULT false,
    PRIMARY KEY (blog_id)
);
"""
