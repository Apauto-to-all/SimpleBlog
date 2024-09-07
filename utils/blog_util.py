# 博客的工具
from db.connection import DatabaseOperation

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
    {
        "blog_id": 1,  # 博客id
        "title": "博客标题",
        "content": "博客内容",
        "username": "用户名",
        "views": 0,
        "likes": 0,
        "created_at": "2021-01-01 00:00:00",
        "is_public": True,
    }
    return blog_info
