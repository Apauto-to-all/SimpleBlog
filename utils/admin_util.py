# 管理员工具
import time
from db.connection import DatabaseOperation

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

operate = DatabaseOperation()


# 获取所有用户信息，返回一个列表，从 start 开始，数量为 count
async def get_all_users(start: int, count: int):
    """
    获取所有用户信息
    :param start: 开始位置
    :param count: 获取用户数量
    :return: 用户信息列表
    """
    logger.info("开始获取所有用户信息")
    users_list = await operate.users_select_all(start, count)
    # 去除密码信息
    for user_info in users_list:
        user_info.pop("password")
    # 添加是否禁言，以及禁言结束时间，以及禁言剩余时间
    for user_info in users_list:
        # 判断用户是否被禁言
        user_info["is_forbid"] = await is_forbid_user(user_info["username"])
        now_time = int(time.time())
        # 禁言结束时间
        user_info["forbid_end_time"] = (
            await get_forbid_end_time(user_info["username"])
            if user_info["is_forbid"]
            else -1
        )
        # 禁言剩余时间
        user_info["forbid_remaining_time"] = (
            user_info["forbid_end_time"] - now_time if user_info["is_forbid"] else -1
        )
        # 如果被禁言，转化为时间格式
        if user_info["is_forbid"]:
            user_info["forbid_end_time"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(user_info["forbid_end_time"])
            )
            user_info["forbid_remaining_time"] = time.strftime(
                "%H:%M:%S", time.gmtime(user_info["forbid_remaining_time"])
            )
    [
        {
            "username": "test",
            "nickname": "测试用户",
            "is_forbid": False,
            "forbid_end_time": -1,
            "forbid_remaining_time": -1,
        },
        {
            "username": "test2",
            "nickname": "测试用户2",
            "is_forbid": True,
            "forbid_end_time": "2021-07-01 00:00:00",
            "forbid_remaining_time": "00:00:00",
        },
    ]
    return users_list


# 获取所有用户数量
async def get_all_users_count():
    """
    获取所有用户数量
    :return: 用户数量
    """
    logger.info("开始获取所有用户数量")
    count = await operate.users_count()
    return count


# 禁言用户
async def forbid_user(username: str, minutes: int):
    """
    禁言用户
    :param username: 用户名
    :param minutes: 禁言时长
    :return: 是否成功
    """
    logger.info(f"开始禁言用户 {username} {minutes} 分钟")
    # 获取当前时间
    current_time = int(time.time())
    # 计算禁言结束时间
    end_time = current_time + minutes * 60
    # 禁言用户
    result = await operate.forbid_user(username, end_time)
    if result:
        return True
    return False


# 判断用户是否被禁言
async def is_forbid_user(username: str):
    """
    判断用户是否被禁言
    :param username: 用户名
    :return: 是否被禁言
    """
    logger.info(f"判断用户 {username} 是否被禁言")
    if await operate.is_forbid_user(username):
        return True
    return False


# 获取用户禁言结束时间
async def get_forbid_end_time(username: str):
    """
    获取用户禁言结束时间
    :param username: 用户名
    :return: 禁言结束时间
    """
    logger.info(f"获取用户 {username} 禁言结束时间")
    end_time = await operate.get_forbid_end_time(username)
    return end_time if end_time else -1


# 解除用户禁言
async def unforbid_user(username: str):
    """
    解除用户禁言
    :param username: 用户名
    :return: 是否成功
    """
    logger.info(f"解除用户 {username} 禁言")
    result = await operate.unforbid_user(username)
    if result:
        return True
    return False


# 禁止博客公开
async def forbid_blog(blog_id: int):
    """
    禁止博客公开
    :param blog_id: 博客 id
    :return: 是否成功
    """
    result = await operate.forbid_blog(blog_id)
    await operate.blogs_set_private(blog_id)
    if result:
        return True
    return False


# 解除博客禁止公开
async def unforbid_blog(blog_id: int):
    """
    解除博客禁止公开
    :param blog_id: 博客 id
    :return: 是否成功
    """
    result = await operate.unforbid_blog(blog_id)
    if result:
        return True
    return False


# 判断博客是否被禁止公开
async def is_forbid_blog(blog_id: int):
    """
    判断博客是否被禁止公开
    :param blog_id: 博客 id
    :return: 是否被禁止公开
    """
    if await operate.is_forbid_blog(blog_id):
        return True
    return False
