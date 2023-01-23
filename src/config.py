class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'V!sionmysql-2023'
    MYSQL_DB = 'flask_login'


config = {
    'development': DevelopmentConfig
}
