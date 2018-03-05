class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    COLLECTION = 'dev'

class ProductionConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    COLLECTION = 'materials'

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    COLLECTION = 'testing'
