import os

class Config:
    SECTCRE_KEY = 'sakib1234'
    Project_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(Project_dir,'data','data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False