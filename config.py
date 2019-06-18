class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret key'
    TESTING = False

class Development(Config):
    DEBUG = True

class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

class Testing(Config):
    """Configurations for testing."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing,
    'default': Config
}

