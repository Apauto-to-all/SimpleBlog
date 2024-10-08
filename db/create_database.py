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


# asyncio.run(create_database())


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
    头像路径 - 用户头像的路径，可以为空
    """
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        username varchar(15) NOT NULL,
        password varchar(60) NOT NULL,
        nickname varchar(20) NOT NULL,
        avatar_path text,
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
    最后修改时间 - 默认为当前时间
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
        created_at timestamptz DEFAULT current_timestamp,
        last_modified timestamptz DEFAULT current_timestamp,
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

    # 创建用户禁言表
    """
    用户禁言表：
    用户名 - 外键，关联用户表
    结束时间 - 禁言结束时间，使用int（time.time()）存储
    """
    sql = """
    CREATE TABLE IF NOT EXISTS forbid_users (
        username varchar(15) REFERENCES users(username) not null,
        end_time int not null,
        PRIMARY KEY (username)
    );
    """
    await conn.execute(sql)

    # 创建博客禁止公开表
    """
    博客禁止公开表：
    博客id - 外键，关联博客表
    """
    sql = """
    CREATE TABLE IF NOT EXISTS forbid_blogs (
        blog_id int REFERENCES blogs(blog_id) not null,
        PRIMARY KEY (blog_id)
    );
    """
    await conn.execute(sql)

    # 是否是管理员表
    """
    管理员表，在表中的都是管理员：
    用户名 - 外键，关联用户表
    持续时间 - 管理员持续时间，使用int（time.time()）存储
    """
    sql = """
    CREATE TABLE IF NOT EXISTS admins (
        username varchar(15) REFERENCES users(username) not null,
        end_time int not null,
        PRIMARY KEY (username)
    );
    """
    await conn.execute(sql)

    # 创建一个需要审核的博客表格，用于存储需要审核的博客
    """
    需要审核的博客表：
    博客id - 外键，关联博客表
    博客添加时间 - 使用时间戳存储，int（time.time()）格式
    是否被审核 - 管理员是否审核博客，true为已审核，false为未审核，默认为false
    审核状态 - 是否审核通过，true为通过，false为未通过，默认为空
    审核时间 - 使用时间戳存储，int（time.time()）格式
    审核人 - 外键，关联用户表
    """
    sql = """
    CREATE TABLE IF NOT EXISTS need_check_blogs (
        blog_id int REFERENCES blogs(blog_id) not null,
        add_time int,
        is_check boolean DEFAULT false,
        is_pass boolean,
        check_time int,
        check_user varchar(15) REFERENCES users(username),
        PRIMARY KEY (blog_id)
    );
    """
    await conn.execute(sql)

    await conn.close()


asyncio.run(create_tables())
