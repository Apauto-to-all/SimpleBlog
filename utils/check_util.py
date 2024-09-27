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
    for blog in checked_blogs_list:
        blog["add_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(blog["add_time"])
        )
        blog["check_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(blog["check_time"])
        )
    return checked_blogs_list


# 获取所有已经审核的博客
async def get_checked_blogs():
    """
    获取所有已经审核的博客
    :return: 返回所有已经审核的博客
    """
    logger.info("开始获取所有已经审核的博客")
    checked_blogs_list = await operate.need_check_blogs_get_checked()
    # 添加博客内容
    [
        {
            "blog_id": 1,  # 博客id
            "add_time": "2021-01-01 00:00:00",  # 添加时间
            "is_check": False,  # 是否审核
            "is_pass": False,  # 是否通过审核
            "check_time": "2021-01-01 00:00:00",  # 审核时间
            "check_user": None,  # 审核人
        }
    ]
    return await format_blog(checked_blogs_list)


# 获取所有已经审核的博客数量
async def get_checked_blogs_count():
    """
    获取所有已经审核的博客数量
    :return: 返回所有已经审核的博客数量
    """
    checked_blogs_count = await operate.need_check_blogs_get_checked_count()
    return checked_blogs_count


# 获取所有需要审核的博客
async def get_need_check_blogs():
    """
    获取所有需要审核的博客
    :return: 返回所有需要审核的博客
    """
    need_check_blogs_list = await operate.need_check_blogs_get_not_check()
    # 添加博客内容
    [
        {
            "blog_id": 1,  # 博客id
            "add_time": "2021-01-01 00:00:00",  # 添加时间
            "is_check": False,  # 是否审核
            "is_pass": False,  # 是否通过审核
            "check_time": "2021-01-01 00:00:00",  # 审核时间
            "check_user": None,  # 审核人
        }
    ]
    return await format_blog(need_check_blogs_list)


# 获取所有需要审核的博客数量
async def get_need_check_blogs_count():
    """
    获取所有需要审核的博客数量
    :return: 返回所有需要审核的博客数量
    """
    need_check_blogs_count = await operate.need_check_blogs_get_check_count()
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
