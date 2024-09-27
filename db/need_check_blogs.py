from re import T
import time
import traceback
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class NeedCheckBlogs:
    # 添加需要审核的博客，默认为未审核
    async def need_check_blogs_insert(self, blog_id: int):
        """
        添加需要审核的博客
        :param blog_id: 博客id，如果博客id已经存在，先删除再添加
        :return: 添加成功返回True，添加失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                delete_sql = """
                DELETE FROM need_check_blogs WHERE blog_id = $1;
                """
                await conn.execute(delete_sql, blog_id)

                sql = """
                INSERT INTO need_check_blogs (blog_id, add_time) 
                VALUES ($1, $2);
                """
                await conn.execute(sql, blog_id, int(time.time()))
                logger.info(f"博客-{blog_id}添加需要审核成功！")
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    # 管理员已经审核
    async def need_check_blogs_pass(self, blog_id: int, check_user: str, is_pass: bool):
        """
        管理员通过审核
        :param blog_id: 博客id
        :param check_user: 审核人
        :return: 通过审核成功返回True，通过审核失败返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                UPDATE need_check_blogs
                SET is_check = true, is_pass = $1, check_time = $2, check_user = $3
                WHERE blog_id = $4;
                """
                await conn.execute(sql, is_pass, int(time.time()), check_user, blog_id)
                return True
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    # 获取所有博客信息，包括未审核和已审核的博客
    async def need_check_blogs_get_not_check(self):
        """
        获取所有未审核的博客
        :return: 返回所有未审核的博客
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT * FROM need_check_blogs WHERE is_check = false;
                """
                blog_ids = await conn.fetch(sql)
                return blog_ids
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []

    # 获取所有未审核的博客数量
    async def need_check_blogs_get_not_check_count(self):
        """
        获取所有未审核的博客数量
        :return: 返回所有未审核的博客数量
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT COUNT(*) FROM need_check_blogs WHERE is_check = false;
                """
                blog_ids = await conn.fetchval(sql)
                return blog_ids
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return 0

    # 获取所有已审核的博客信息
    async def need_check_blogs_get_check(self):
        """
        获取所有已审核的博客
        :return: 返回所有已审核的博客
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT * FROM need_check_blogs WHERE is_check = true;
                """
                blog_ids = await conn.fetch(sql)
                return blog_ids
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return []

    # 获取所有已审核的博客数量
    async def need_check_blogs_get_check_count(self):
        """
        获取所有已审核的博客数量
        :return: 返回所有已审核的博客数量
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT COUNT(*) FROM need_check_blogs WHERE is_check = true;
                """
                blog_ids = await conn.fetchval(sql)
                return blog_ids
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return 0

    # 博客是否被审核
    async def need_check_blogs_is_check(self, blog_id: int):
        """
        博客是否被审核
        :param blog_id: 博客id
        :return: 已审核返回True，未审核返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT is_check, blog_id
                FROM need_check_blogs 
                WHERE blog_id = $1;
                """
                info = await conn.fetchval(sql, blog_id)
                if info is None:
                    return True
                return info.get("is_check")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False

    # 博客是否通过
    async def need_check_blogs_is_pass(self, blog_id: int):
        """
        博客是否通过
        :param blog_id: 博客id
        :return: 通过返回True，未通过返回False
        """
        async with self.pool.acquire() as conn:
            try:
                sql = """
                SELECT is_pass, blog_id
                FROM need_check_blogs 
                WHERE blog_id = $1;
                """
                info = await conn.fetchval(sql, blog_id)
                if info is None:
                    return True
                return info.get("is_pass")
            except Exception as e:
                error_info = traceback.format_exc()
                logger.error(error_info)
                logger.error(e)
                return False


# 创建一个需要审核的博客表格，用于存储需要审核的博客
"""
需要审核的博客表：
博客id - 外键，关联博客表
博客添加时间 - 使用时间戳存储，int（time.time()）格式
是否被审核 - 管理员是否审核博客，true为已审核，false为未审核，默认为false
审核状态 - 是否审核通过，true为通过，false为未通过，默认为空
审核时间 - 使用时间戳存储，int（time.time()）格式
审核人 - 外键，关联用户表
"""
sql = """
CREATE TABLE IF NOT EXISTS need_check_blogs (
    blog_id int REFERENCES blogs(blog_id) not null,
    add_time int,
    is_check boolean DEFAULT false,
    is_pass boolean,
    check_time int,
    check_user varchar(15) REFERENCES users(username),
    PRIMARY KEY (blog_id)
);
"""
