from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create engine and session
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Successfully connected to database")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    character_class = Column(String)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    workouts = relationship("Workout", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=datetime.now().date())
    exercise = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    exp_gained = Column(Integer)
    user = relationship("User", back_populates="workouts")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    image_url = Column(String)
    exp_reward = Column(Integer)
    users = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    date_earned = Column(Date, default=datetime.now().date())
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Successfully created database tables")
except Exception as e:
    logger.error(f"Failed to create database tables: {str(e)}")
    raise