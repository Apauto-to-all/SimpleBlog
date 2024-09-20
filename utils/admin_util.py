# 管理员工具
from db.connection import DatabaseOperation

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

users_operate = DatabaseOperation()


# 获取所有用户信息，返回一个列表
async def get_all_users(start, count):
    """
    获取所有用户信息
    :param start: 起始位置
    :param count: 获取数量
    :return: 用户信息列表
    """
    logger.info("开始获取所有用户信息")
    users_list = await users_operate.users_select_all(start, count)
    [
        {
            "username": "admin",
            "password": "admin",
            "nickname": "管理员",
        },
        {
            "username": "test",
            "password": "test",
            "nickname": "测试用户",
        },
    ]
    return users_list
