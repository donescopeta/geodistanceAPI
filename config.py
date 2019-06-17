class Config:
	SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	DEBUG = False
	CSRF_ENABLED = True
	ECRET_KEY = 'secret key'

class Development(Config):
	DEBUG = True

class Production(Config):
    """Configurations for Production."""
    DEBUG = False

class Testing(Config):
	"""Configurations for Production."""
	TESTING = True
	DEBUG = True

app_config = {
    'development': Development,
    'production': Production,
	'testing': Testing,
	'default': Config
}

