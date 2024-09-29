# 检查工具类
import time
from db.connection import DatabaseOperation

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

operate = DatabaseOperation()


# 插入需要审核的博客
async def insert_need_check_blogs(blog_id: int):
    """
    插入需要审核的博客
    :param blog_id: 博客id
    :return: 添加成功返回True，添加失败返回False
    """
    result = await operate.need_check_blogs_insert(blog_id)
    if result:
        return True
    else:
        return False


# 博客格式化
async def format_blog(checked_blogs_list: dict) -> dict:
    formatted_blogs = []
    for blog in checked_blogs_list:
        blog_dict = dict(blog)  # 将 asyncpg.Record 转换为字典
        if "add_time" in blog:
            blog_dict["add_time"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(blog.get("add_time"))
            )
        else:
            blog_dict["add_time"] = -1
        if "check_time" in blog:
            blog_dict["check_time"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(blog.get("check_time"))
            )
        else:
            blog_dict["check_time"] = -1

        blog_id = blog["blog_id"]
        blog_info = await operate.blogs_select(blog_id)

        blog_dict["title"] = blog_info.get("title")
        blog_dict["content"] = blog_info.get("content")
        blog_dict["username"] = blog_info.get("username")

        blog_dict["tags"] = await operate.tags_select(blog_id)
        formatted_blogs.append(blog_dict)
    [
        {
            "blog_id": 1,
            "title": "博客标题",
            "content": "博客内容",
            "username": "博客作者",
            "tags": ["标签1", "标签2"],
            "add_time": "2021-07-01 12:00:00",
            "check_time": "2021-07-01 12:00:00",
            "is_pass": True,
            "is_check": True,
            "check_user": "审核人",
        }
    ]
    return formatted_blogs


# 获取所有已经审核的博客
async def get_checked_blogs(start: int, count: int, is_pass: str = None):
    """
    获取所有已经审核的博客
    :param start: 开始位置
    :param count: 获取数量
    :return: 返回所有已经审核的博客
    """
    logger.info("开始获取所有已经审核的博客")
    checked_blogs_list = await operate.need_check_blogs_get_checked(
        start, count, is_pass
    )
    return await format_blog(checked_blogs_list)


# 获取所有已经审核的博客数量
async def get_checked_blogs_count():
    """
    获取所有已经审核的博客数量
    :return: 返回所有已经审核的博客数量
    """
    checked_blogs_count = await operate.need_check_blogs_get_checkde_count()
    return checked_blogs_count


# 获取所有需要审核的博客
async def get_need_check_blogs(start: int, count: int):
    """
    获取所有需要审核的博客
    :param start: 开始位置
    :param count: 获取数量
    :return: 返回所有需要审核的博客
    """
    need_check_blogs_list = await operate.need_check_blogs_get_not_check(start, count)
    return await format_blog(need_check_blogs_list)


# 获取所有需要审核的博客数量
async def get_need_check_blogs_count():
    """
    获取所有需要审核的博客数量
    :return: 返回所有需要审核的博客数量
    """
    need_check_blogs_count = await operate.need_check_blogs_get_not_check_count()
    return need_check_blogs_count


# 管理员审核博客
async def pass_check_blog(blog_id: int, check_user: str, is_pass: bool):
    """
    博客审核通过
    :param blog_id: 博客id
    :param check_user: 审核人
    :param is_pass: 是否通过审核
    :return: 通过审核成功返回True，通过审核失败返回False
    """
    result = await operate.need_check_blogs_pass(blog_id, check_user, is_pass)
    if result:
        if is_pass:
            # 如果通过审核，设置博客为公开
            await operate.blogs_set_public(blog_id)
        return True
    else:
        return False


# 博客是否被审核
async def is_check_blog(blog_id: int):
    """
    博客是否被审核
    :param blog_id: 博客id
    :return: 博客已经审核返回True，博客未审核返回False
    """
    result = await operate.need_check_blogs_is_check(blog_id)
    return result


# 博客是否通过
async def is_pass_blog(blog_id: int):
    """
    博客是否通过
    :param blog_id: 博客id
    :return: 博客已经通过返回True，博客未通过返回False
    """
    result = await operate.need_check_blogs_is_pass(blog_id)
    return result


# 博客是否私有
async def is_private_blog(blog_id: int):
    """
    博客是否需要审核
    :param blog_id: 博客id
    :return: 博客需要审核返回True，博客不需要审核返回False
    """
    if await operate.need_check_blogs_is_exist(blog_id) == False:
        blog_info = await operate.blogs_select(blog_id)
        is_public = blog_info.get("is_public")
        if is_public == False:
            return True

    return False
