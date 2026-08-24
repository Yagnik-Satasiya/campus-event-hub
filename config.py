import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/campus_events_db"  # local fallback
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
