# 创建pgsql数据库以及表
import asyncpg
import asyncio
from private_settings import (
    pgsql_host,
    pgsql_user,
    pgsql_password,
    database_name,
    pgsql_port,
)


# 在PostgreSQL数据库中创建一个数据库——SimpleBlog
async def create_database():
    conn = await asyncpg.connect(
        user=pgsql_user,
        password=pgsql_password,
        host=pgsql_host,
        port=pgsql_port,
    )
    # 创建一个数据库
    await conn.execute(f"CREATE DATABASE {database_name};")
    await conn.close()


asyncio.run(create_database())


# 创建一些表
async def create_tables():
    conn = await asyncpg.connect(
        user=pgsql_user,
        password=pgsql_password,
        host=pgsql_host,
        port=pgsql_port,
        database=database_name,
    )
    # 创建一个用户表
    """
    用户表：
    用户名（id）- 主键，用户自定义，使用字母+数字，唯一，2-15位
    密码 - 4-15位，包含字母和数字，加密后60位
    昵称 - 2-20位，不包含特殊字符
    """
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        username varchar(15) NOT NULL,
        password varchar(60) NOT NULL,
        nickname varchar(20) NOT NULL,
        PRIMARY KEY (username)
    );
    """
    await conn.execute(sql)
    # 创建一个博客表
    """
    博客表：
    博客id - 主键，自增
    博客标题 - 2-50位
    博客内容 - 无限制
    博客作者 - 外键，关联用户表
    阅读量 - 默认为0
    点赞量 - 默认为0
    发布时间 - 默认为当前时间
    是否公开 - 默认为不公开，false
    """
    sql = """
    CREATE TABLE IF NOT EXISTS blogs (
        blog_id serial,
        title varchar(50) NOT NULL,
        content text,
        username varchar(15) REFERENCES users(username) not null,
        views int DEFAULT 0,
        likes int DEFAULT 0,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        is_public boolean DEFAULT false,
        PRIMARY KEY (blog_id)
    );
    """
    await conn.execute(sql)
    # 创建一个标签表
    """
    标签表：
    标签 - 自定义，2-30位
    博客id - 外键，关联博客表
    二者联合主键
    """
    sql = """
    CREATE TABLE IF NOT EXISTS tags (
        tag varchar(30) NOT NULL,
        blog_id int REFERENCES blogs(blog_id),
        PRIMARY KEY (tag, blog_id)
    );
    """
    await conn.execute(sql)
    # 创建一一个标签视图，用于查询标签，所有标签和对应的博客数量
    """
    标签视图：
    标签 - 自定义，2-30位
    博客数量 - 该标签对应的博客数量
    """
    # 检查视图是否存在的 SQL 语句
    check_view_sql = """
    SELECT EXISTS (
        SELECT 1
        FROM pg_views
        WHERE viewname = 'tag_view'
    );
    """
    # 检查视图是否存在
    view_exists = await conn.fetchval(check_view_sql)

    sql = """
    CREATE VIEW tag_view AS
    SELECT tag, COUNT(blog_id) AS blog_count
    FROM tags
    GROUP BY tag
    ORDER BY blog_count DESC;
    """

    # 如果视图不存在，则创建视图
    if not view_exists:
        await conn.execute(sql)

    await conn.close()


asyncio.run(create_tables())


# 插入博客并获取自增ID
async def insert_blog(title, content):
    conn = await asyncpg.connect(
        user=pgsql_user,
        password=pgsql_password,
        host=pgsql_host,
        port=pgsql_port,
        database=database_name,
    )
    sql = """
    INSERT INTO blogs (title, content) VALUES ($1, $2) RETURNING blog_id;
    """
    blog_id = await conn.fetchval(sql, title, content)
    await conn.close()
    return blog_id
