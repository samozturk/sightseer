from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

from models import User, Destination, Base
DB_NAME = 'sightseer.db'

def init_db(db_name=DB_NAME):
    engine = create_engine('sqlite:///' + db_name, echo=False)
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)
    return session

def insert_user(new_user:User):
    session = init_db()
    session.add(new_user)
    session.commit()
    session.close()

def get_users():
    session = init_db()
    users = session.query(User).all()
    users_dict = [user.__dict__ for user in users]
    for user in users_dict:
        user.pop('_sa_instance_state', None)
    session.close()
    return users_dict

def get_destionations():
    session = init_db()
    destionations = session.query(Destination).all()
    destionations_dict = [destionation.__dict__ for destionation in destionations]
    for destionation in destionations_dict:
        destionation.pop('_sa_instance_state', None)
    session.close()
    return destionations_dict

init_db()

new_user = User(name='John Doe',email="x.com",password="1234")
insert_user(new_user)
users = get_users()
print(users)
df = pd.DataFrame(users)
print(df)