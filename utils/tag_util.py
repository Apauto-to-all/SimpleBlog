# 标签工具
from db.connection import DatabaseOperation
import logging
from .blog_util import get_new_blogs_list

logger = logging.getLogger(__name__)

# 创建一个数据库操作对象
blogs_operation = DatabaseOperation()


async def get_best_tags() -> list:
    """
    获取最佳的tag标签，前10个
    :return: tag标签列表
    """
    tags_dict = await blogs_operation.tags_select_view()
    {
        "标签1": 1,  # 标签1的博客数量
        "标签2": 2,  # 标签2的博客数量
    }
    tags_list = list(tags_dict.keys())
    # 获取前10个标签
    return tags_list[:10]


async def get_tag_search_list(tags_list: list, start: int, count: int) -> list:
    """
    获取标签搜索列表
    :param tags_list: 标签列表
    :param start: 起始位置
    :param count: 获取博客数量
    :return: 返回博客信息列表
    """
    blog_list = await blogs_operation.tags_select_blog(tags_list, start, count)
    [
        {
            "blog_id": 1,  # 博客id
            "title": "博客标题1",  # 博客标题
            "content": "博客内容1",  # 博客内容
            "username": "博客作者1",  # 博客作者
            "views": 1,  # 阅读量
            "likes": 1,  # 点赞量
            "created_at": "2021-01-01 00:00:00",  # 发布时间
            "last_modified": "2021-01-01 00:00:00",  # 最后修改时间
            "is_public": True,  # 是否公开
            "is_forbid_blog": False,  # 是否被禁止公开
        }
    ]
    return await get_new_blogs_list(blog_list)
