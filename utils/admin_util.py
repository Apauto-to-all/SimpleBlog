# 管理员工具
from db.connection import DatabaseOperation

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

users_operate = DatabaseOperation()


# 获取所有用户信息，返回一个列表
async def get_all_users():
    """
    获取所有用户信息
    :return: 用户信息列表
    """
    logger.info("开始获取所有用户信息")
    users_list = await users_operate.users_select_all()
    # 去除密码信息
    for user_info in users_list:
        user_info.pop("password")
    [
        {
            "username": "admin",
            "nickname": "管理员",
        },
        {
            "username": "test",
            "nickname": "测试用户",
        },
    ]
    return users_list
