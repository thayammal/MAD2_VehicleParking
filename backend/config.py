class Config():
    SECURITY_LOGIN_URL = '/SiGnIn'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'


class localDev(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = "Shhhhh.... its a secret"
    SECURITY_JOIN_USER_ROLES = True

    SECURITY_TOKEN_EXPIRE_TIMESTAMP = lambda user: 0  # 0 means never expiries
    SECURITY_TOKEN_MAX_AGE = None  # None for no expiration

    DEBUG = True

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 2
    CACHE_KEY_PREFIX = 'MyAppCache'
    CACHE_DEFAULT_TIMEOUT = 60 #IN SEC

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'donot_reply@abc.com'


class production(Config):
    DEBUG = False

class CeleryConfig():
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    task_serializer = 'json'
    timezone = 'Asia/Kolkata'