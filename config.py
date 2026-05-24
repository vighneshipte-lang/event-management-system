class Config:
    SECRET_KEY = 'mini_project_VSM'

    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:vighnesh123@localhost/event_management_system'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False