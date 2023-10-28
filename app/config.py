import os

secret_key = '8567ccr7d2daa4d9c7f952d1cca92b6c9183e5907262017d986e43ef18422638'

sqlalchemy_track_modifications = False

sqlalchemy_database_uri = 'mysql+mysqlconnector://std_1960_stephane_e-library:qwertyqq@std-mysql.ist.mospolytech.ru/std_1960_stephane_e-library'

sqlalchemy_echo = True

upload_folder = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'img', 'image')
