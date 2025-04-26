from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    clicks = Column(Integer, default=0)
    multiplier = Column(Integer, default=1)
    last_click_time = Column(DateTime)

engine = create_engine('sqlite:///clicks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_user(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                username=f"User_{user_id}",
                last_click_time=datetime.datetime.now()
            )
            session.add(user)
            session.commit()
        return user

def update_clicks(user_id: int, clicks: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.clicks = clicks
        session.commit()

def buy_multiplier(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        cost = 50 * user.multiplier
        if user.clicks >= cost:
            user.clicks -= cost
            user.multiplier += 1
            session.commit()
            return True
        return False