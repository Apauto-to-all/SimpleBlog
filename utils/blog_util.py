# 博客的工具
from db.connection import DatabaseOperation
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# 创建一个数据库操作对象
blogs_operation = DatabaseOperation()


# 通过博客的id获取博客的信息
async def get_blog_info(blog_id: int) -> dict:
    """
    通过博客的id获取博客的信息
    :param blog_id: 博客id
    :return: 博客信息
    """
    blog_info = await blogs_operation.blogs_select(blog_id)
    tags_list = await blogs_operation.tags_select(blog_id)
    if blog_info and tags_list:
        blog_info["tags"] = tags_list
        user_info = await blogs_operation.users_select(blog_info.get("username"))
        blog_info["nickname"] = user_info.get("nickname")
        blog_info["created_at"] = blog_info["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        {
            "blog_id": 1,  # 博客id
            "title": "博客标题",
            "content": "博客内容",
            "username": "用户名",
            "nickname": "昵称",
            "views": 0,
            "likes": 0,
            "created_at": "2021-01-01 00:00:00",
            "tags": ["标签1", "标签2"],
        }
        return blog_info

    return {}


# 写入博客，返回博客id
async def write_blog(
    username: str, title: str, content: str, tags: str, is_public: bool
) -> int:
    """
    写入博客，返回博客id
    :param username: 用户名
    :param title: 博客标题
    :param content: 博客内容
    :param tags: 博客标签
    :param is_public: 是否公开
    :return: 博客id
    """
    if not tags:
        logger.error("标签为空！")
        return -1
    # 切割标签为列表，中文逗号或英文逗号，都可以
    tags_list = tags.replace("，", ",").split(",")
    # 写入草稿博客
    blog_id = await blogs_operation.blogs_insert_draft(title, content, username)
    if not blog_id:
        logger.error("博客写入失败！")
        return -1
    if is_public:
        if not await blogs_operation.blogs_set_public(blog_id):
            logger.error("博客设置公开失败！")
            return -1
    if not await blogs_operation.tags_insert(tags_list, blog_id):
        logger.error("博客标签写入失败！")
        return -1

    return blog_id


# 博客浏览量加一
async def blog_views_add_one(blog_id: int):
    """
    博客浏览量加一
    :param blog_id: 博客id
    """
    return await blogs_operation.blogs_views_add_one(blog_id)


# 博客点赞量加一
async def blog_likes_add_one(blog_id: int):
    """
    博客点赞量加一
    :param blog_id: 博客id
    """
    return await blogs_operation.blogs_likes_add_one(blog_id)


# 博客点赞量减一
async def blog_likes_sub_one(blog_id: int):
    """
    博客点赞量减一
    :param blog_id: 博客id
    """
    return await blogs_operation.blogs_likes_sub_one(blog_id)
