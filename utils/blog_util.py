# 博客的工具
from db.connection import DatabaseOperation
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# 创建一个数据库操作对象
blogs_operation = DatabaseOperation()


# 通过博客的id获取博客的信息，无论是否公开
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
        blog_info["last_modified"] = blog_info["last_modified"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        {
            "blog_id": 1,  # 博客id
            "title": "博客标题",
            "content": "博客内容",
            "username": "用户名",
            "nickname": "昵称",
            "views": 0,
            "likes": 0,
            "created_at": "2021-01-01 00:00:00",  # 发布时间
            "last_modified": "2021-01-01 00:00:00",  # 最后修改时间
            "tags": ["标签1", "标签2"],
            "is_public": True or False,
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


# 更新博客
async def revise_blog(
    blog_id: int, title: str, content: str, tags: str, is_public: bool
) -> bool:
    """
    更新博客
    :param blog_id: 博客id
    :param title: 博客标题
    :param content: 博客内容
    :param tags: 博客标签
    :param is_public: 是否公开
    :return: 更新成功返回True，更新失败返回False
    """
    if (
        not blog_id
        or not isinstance(blog_id, int)
        or not title
        or not content
        or not tags
        or not is_public
        or not isinstance(is_public, bool)
    ):
        logger.error("参数错误！")
        return False
    # 切割标签为列表，中文逗号或英文逗号，都可以
    tags_list = tags.replace("，", ",").split(",")
    await blogs_operation.blogs_update(blog_id, title, content)
    await blogs_operation.tags_insert(tags_list, blog_id)
    if is_public:
        await blogs_operation.blogs_set_public(blog_id)

    return True


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


# 获取博客信息列表，但时间，热度，最佳
async def get_blogs_list(blog_type: str, start: int, count: int) -> list:
    """
    获取博客信息
    :param blog_type: 博客类型 ('new', 'hot', 'hot_month', 'best')
    :param start: 起始位置
    :param count: 获取博客数量
    :return: 博客信息列表
    """
    blogs_list = await blogs_operation.blogs_select_list(blog_type, start, count)
    return await get_new_blogs_list(blogs_list)


# 获取用户创作的博客信息列表
async def get_user_blogs_list(
    username: str, start: int, count: int, is_all: bool = False
) -> list:
    """
    获取用户创作的博客信息列表
    :param username: 用户名
    :param start: 起始位置
    :param count: 获取博客数量
    :param is_all: 是否获取全部博客，只有用户自己可以获取全部博客，默认为False
    :return: 博客信息列表
    """
    blogs_list = await blogs_operation.blogs_select_list_by_username(
        username, start, count, is_all
    )
    return await get_new_blogs_list(blogs_list)


# 放回新博客列表工具
async def get_new_blogs_list(blogs_list: list) -> list:
    new_blogs_list = []
    for blog_info in blogs_list:
        user_info = await blogs_operation.users_select(blog_info.get("username"))
        blog_dict = {
            "blog_id": blog_info.get("blog_id"),  # 博客id
            "title": blog_info.get("title"),  # 博客标题
            "content": blog_info.get("content"),  # 博客内容
            "username": blog_info.get("username"),  # 博客作者
            "nickname": user_info.get("nickname"),  # 博客作者昵称
            "views": blog_info.get("views"),  # 阅读量
            "likes": blog_info.get("likes"),  # 点赞量
            "created_at": blog_info.get("created_at").strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # 发布时间
            "last_modified": blog_info.get("last_modified").strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # 最后修改时间
            "tags": await blogs_operation.tags_select(blog_info.get("blog_id")),
            "is_public": blog_info.get("is_public"),
        }
        new_blogs_list.append(blog_dict)
    return new_blogs_list
