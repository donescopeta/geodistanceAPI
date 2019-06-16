class Config:
	SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
	DEBUG = False
	CSRF_ENABLED = True

class Development(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
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

