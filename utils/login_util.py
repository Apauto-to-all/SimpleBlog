# 登入，注册，登出的工具类
import jwt  # 导入jwt模块
from datetime import datetime, timedelta, timezone
from private_settings import SECRET_KEY, login_time_minute
import bcrypt
from db.connection import DatabaseOperation

import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

users_operate = DatabaseOperation()


# 加密密码
async def encrypt_password(password: str) -> str:
    """
    :param password: 密码
    :return: 返回加密后的密码
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # 返回加密后的密码，长度为60位


# 验证密码
async def verify_password(hashed_password: str, password: str) -> bool:
    """
    :param hashed_password: 加密后的密码
    :param password: 密码
    :return: 返回密码是否正确，True表示密码正确，False表示密码错误
    """
    try:
        return bcrypt.checkpw(
            password.encode(), hashed_password.encode()
        )  # 返回True或False，表示密码是否正确
    except Exception as e:
        return False  # 返回False，表示密码错误


# 注册用户
async def register_user(username, password, confirm_password, nickname):
    """
    注册用户
    :param username: 用户名
    :param password: 密码
    :param confirm_password: 确认密码
    :param nickname: 昵称
    :return: 注册成功返回True，注册失败返回False
    """
    logger.info("开始处理注册请求")
    if not username or not password or not confirm_password or not nickname:
        logger.info(
            "用户名: %s, 密码: %s, 确认密码: %s, 昵称: %s",
            username,
            password,
            confirm_password,
            nickname,
        )
        logger.error("用户名、密码、确认密码、昵称为空，注册失败！")
        return False
    if password != confirm_password:
        logger.error("密码和确认密码不一致！注册失败！")
        return False
    # 用户名和密码只能包含字母和数字
    if not username.isalnum():
        logger.error("用户名包含除了字母和数字之外的字符！注册失败！")
        return False
    if not (2 <= len(username) <= 15):
        logger.error("用户名长度不符合要求！注册失败！")
        return False
    if not (4 <= len(password) <= 15):
        logger.error("密码长度不符合要求！注册失败！")
        return False
    if not (2 <= len(nickname) <= 20):
        logger.error("昵称长度不符合要求！注册失败！")
        return False
    hashed_password = await encrypt_password(password)
    if not await users_operate.users_insert(username, hashed_password, nickname):
        logger.error("注册失败")
        return False
    return True


# 登入用户
async def login_user(username, password):
    """
    登入用户
    :param username: 用户名
    :param password: 密码
    :return: 登入成功返回True，登入失败返回False
    """
    # 获取用户密码
    hashed_password = await users_operate.users_select_password(username)
    if not hashed_password:
        logger.error("用户不存在！登入失败！")
        return False
    if await verify_password(hashed_password, password):
        logger.info("登入成功！")
        return True
    logger.error("密码错误！登入失败！")
    return False


ALGORITHM = "HS256"  # 加密算法


# 生成JWT
async def get_access_jwt(user: str) -> str:
    """
    生成JWT
    :param user: 用户信息
    :return: JWT Token
    """
    import secrets

    payload = {
        "jti": secrets.token_hex(16),  # JWT ID
        "user": user,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=login_time_minute),  # 使用带有UTC时区信息的datetime对象
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # 生成token
    return access_token


# 验证JWT
async def get_user_from_jwt(token: str) -> str:
    """
    验证JWT，返回用户信息，如果Token无效，返回空字符串
    :param token: JWT Token
    :return: 用户信息，如果Token无效，返回None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 解码token
        return payload.get("user")  # 返回用户信息
    except jwt.ExpiredSignatureError:
        "Token已过期"
        return None
    except jwt.InvalidTokenError:
        "无效的Token"
        return None


# 验证是否登入
async def is_login_get_username(access_token: str) -> str:
    """
    验证是否登入，返回用户名
    :param access_token: JWT Token
    :return: 已登入返回True，未登入返回False
    """
    if not access_token:
        return False
    username = await get_user_from_jwt(access_token)  # 从 JWT 中获取用户名
    if await users_operate.users_select_username(username):
        return username
    return ""
