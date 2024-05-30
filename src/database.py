import os
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '../.env'))

user = os.getenv("DB_USER")
passwd = os.getenv("DB_PASSWORD")
os.environ['TNS_ADMIN'] = '/opt/instantclient_19_22/network/admin'
instant_client_path = "/opt/instantclient_19_22"
cx_Oracle.init_oracle_client(lib_dir=instant_client_path)

tns_name = os.getenv("DB_TNS")

engine = create_engine(
    f'oracle+cx_oracle://:@',
    connect_args={
        'user': user,
        'password': passwd,
        'dsn': tns_name,
    },
    echo=True
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()