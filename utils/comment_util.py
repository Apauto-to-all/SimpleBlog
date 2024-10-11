# 评论相关的工具函数
import time
from db.connection import DatabaseOperation
import logging

logger = logging.getLogger(__name__)

# 创建一个数据库操作对象
operation = DatabaseOperation()


# 发表评论
async def submit_comment(blog_id: int, username: str, comment: str) -> dict:
    """
    发表评论
    :param blog_id: 博客 ID
    :param username: 用户名
    :param comment: 评论内容
    :return: 返回结果
    """
    if await operation.comments_insert(blog_id, username, comment):
        return True
    return False


# 删除评论
async def delete_comment(blog_id: int, username: str, comment_time: int) -> dict:
    """
    删除评论
    :param blog_id: 博客 ID
    :param username: 用户名
    :param comment_time: 评论时间
    :return: 返回结果
    """
    if await operation.comments_delete(blog_id, username, comment_time):
        return True
    return False


# 获取评论
async def get_comments(blog_id: int, start: int, count: int) -> dict:
    """
    获取评论
    :param blog_id: 博客 ID
    :param start: 起始位置
    :param count: 获取评论数量
    :return: 返回结果
    """
    comments = await operation.comments_get(blog_id, start, count)
    return await format_comments(comments)


# 格式化评论
async def format_comments(comments: list) -> list:
    """
    格式化评论
    :param comments: 评论列表
    :return: 返回格式化后的评论列表
    """
    new_comments = []
    for comment in comments:
        comment_dict = dict(comment)  # 将 asyncpg.Record 转换为字典
        comment_dict["comment_time_show"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(comment_dict["comment_time"])
        )
        # 用户信息
        user_dict = await operation.users_select(comment_dict["username"])
        comment_dict["nickname"] = user_dict["nickname"]  # 用户昵称
        # 用户头像
        comment_dict["avatar_url"] = (
            f"/img/avatar/{comment_dict['username']}?t={time.time()}"
        )
        new_comments.append(comment_dict)
    return new_comments
