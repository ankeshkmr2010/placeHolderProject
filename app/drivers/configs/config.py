import os


class Config:
    POSTGRES_HOST:str = ""
    POSTGRES_PORT:str = ""
    POSTGRES_DB:str = ""
    POSTGRES_USER:str = ""
    POSTGRES_PASSWORD:str = ""
    POSTGRES_URL:str = "postgresql+asyncpg://postgres:postgres@localhost:5432/personal"
    YOYO_POSTGRES:str = POSTGRES_URL.replace("+asyncpg", "")
    MONGO_URI:str = "mongodb://localhost:27017"
    MONGO_HOST:str = ""
    MONGO_PORT:str = ""
    MONGO_DBNAME:str = "mydb"
    SVC_ENV:str = "local"
    _populated:str = False


    @staticmethod
    def init_config():
        if Config._populated:
            raise Exception("Config is already populated. Attempting to populate again")
        # populate defaults
        Config._populate_default_config()

        # override with env
        Config.populate_config_from_env()

        # derived config
        Config.populate_derived_config()

        Config._populated = True
        pass

    @staticmethod
    def _populate_default_config():
        Config.POSTGRES_DB = "personal"
        Config.POSTGRES_HOST = "localhost"
        Config.POSTGRES_PORT = "5432"
        Config.POSTGRES_USER = "postgres"
        Config.POSTGRES_PASSWORD = "postgres"
        Config.MONGO_HOST = "localhost"
        Config.MONGO_DBNAME = "mydb"
        Config.MONGO_PORT = "27017"
        pass

    @staticmethod
    def populate_config_from_env():
        python_api_service_env = os.environ.get("PYTHON_API_SERVICE_ENV")
        if not python_api_service_env:
            raise Exception("Missing environment variable PYTHON_API_SERVICE_ENV")
        else:
            Config.SVC_ENV = python_api_service_env

        Config.POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
        Config.POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
        Config.POSTGRES_DB = os.environ.get("POSTGRES_DB")
        Config.POSTGRES_USER = os.environ.get("POSTGRES_USER")
        Config.POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        Config.MONGO_HOST = os.environ.get("MONGO_HOST")
        Config.MONGO_PORT = os.environ.get("MONGO_PORT")
        Config.MONGO_DBNAME = os.environ.get("MONGO_DBNAME")



    @staticmethod
    def populate_derived_config():
        Config.POSTGRES_URL = f"postgresql+asyncpg://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}"
        Config.YOYO_POSTGRES = Config.POSTGRES_URL.replace("+asyncpg", "")
        Config.MONGO_URI = f"mongodb://{Config.MONGO_HOST}:{Config.MONGO_PORT}"



