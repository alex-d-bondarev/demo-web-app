import os

class Config:
    """Configuration for Items Service"""
    
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'icu_v1')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    
    # WireMock
    WIREMOCK_URL = os.getenv('WIREMOCK_URL', 'http://localhost:8080')
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_PORT = os.getenv('FLASK_PORT', 5001)
    DEBUG = FLASK_ENV == 'development'
    
    @staticmethod
    def get_db_connection_string():
        """Get MySQL connection string"""
        return f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
