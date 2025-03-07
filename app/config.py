DB_User = "myuser"
DB_Password = "mypassword"
DB_Host = "db"
DB_Port = "5432"
DB_DataBase = "mydatabase"

class Config:
    """
        Configuration settings for the Flask application.
    """
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_User}:{DB_Password}@{DB_Host}:{DB_Port}/{DB_DataBase}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_BOOKINGS = 2