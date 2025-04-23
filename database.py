from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///clicks.db')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    clicks = Column(Integer, default=0)
    multiplier = Column(Integer, default=1)
    last_click_time = Column(DateTime)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

async def get_user(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id, username="Anonymous")
            session.add(user)
            session.commit()
        return user

async def update_clicks(user_id: int, clicks: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.clicks = clicks
        user.last_click_time = datetime.datetime.now()
        session.commit()

async def buy_multiplier(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        cost = 50 * user.multiplier
        if user.clicks >= cost:
            user.clicks -= cost
            user.multiplier += 1
            session.commit()
            return True
        return False

async def get_leaderboard():
    with Session() as session:
        users = session.query(User).order_by(User.clicks.desc()).limit(10).all()
        return users