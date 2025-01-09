from sqlalchemy import create_engine
from urllib.parse import quote_plus

""" If echo is set to 'True', execute sql will be printed """
password = 'KangoShyVpn500'
safe_password = quote_plus(password)
DATABASE_URI = 'mysql+pymysql://root:' + safe_password + '@103.178.57.34:3306/test'
engine = create_engine(DATABASE_URI, echo=True)
