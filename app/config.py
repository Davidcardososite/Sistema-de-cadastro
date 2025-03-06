# config.py
import pymysql
pymysql.install_as_MySQLdb()


class Config:
    
    # chave secreta
    SECRET_KEY = '32a6404ae504e2482914342c3d4e80b4'

    # banco de dados
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clientes.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    # Configurações adicionais para o pool do banco de dados
    SQLALCHEMY_POOL_RECYCLE = 280  # Reciclar conexões do pool a cada 280 segundos
    SQLALCHEMY_POOL_TIMEOUT = 20   # Tempo limite de espera por uma conexão no pool
    SQLALCHEMY_POOL_SIZE = 10
    # Define o número máximo de conexões persistentes que podem existir simultaneamente no pool.
    SQLALCHEMY_MAX_OVERFLOW = 20
    # Especifica o número máximo de conexões extras que podem ser criadas além do limite definido em



    
    

