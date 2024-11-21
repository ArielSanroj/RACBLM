import streamlit as st
from sqlalchemy import (
    create_engine, Column, Integer, String, 
    DateTime, ForeignKey, Text, Float, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from typing import Optional
import os

# Base class for database models
Base = declarative_base()

# User model for user details
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    service = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# ChatMessage model for storing chat-related messages
class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String(50))

    user = relationship("User", back_populates="messages")

User.messages = relationship("ChatMessage", back_populates="user")

# Archetype model for user archetypes
class Archetype(Base):
    __tablename__ = "archetypes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    characteristics = Column(JSON, nullable=True)  # Characteristics in JSON
    strategies = Column(JSON, nullable=True)  # Strategies for improvement

    subscales = relationship("Subscale", back_populates="archetype")

# Subscale model for coping subscales
class Subscale(Base):
    __tablename__ = "subscales"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    definition = Column(String, nullable=False)
    interpretation = Column(String, nullable=True)
    profile_correlation = Column(JSON, nullable=True)  # Correlation in JSON
    archetype_id = Column(Integer, ForeignKey("archetypes.id"), nullable=False)

    archetype = relationship("Archetype", back_populates="subscales")

# UserResponse model for user test responses
class UserResponse(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Foreign key linking to User
    response_data = Column(JSON, nullable=False)  # User response data in JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# DatabaseManager for managing sessions and connections
class DatabaseManager:
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection."""
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')

        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Create a new database session."""
        return self.SessionLocal()

    def close(self):
        """Close database connection."""
        self.engine.dispose()

# Function to initialize the database and return a session factory
def initialize_database():
    """Initialize the database and return a session factory."""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

# Function to preload data into the database
def preload_data(session):
    """Preload archetypes and subscales into the database for initial setup."""
    try:
        archetypes = [
            {
                "name": "Autonomous",
                "description": "Problem solvers who take charge but may avoid asking for help.",
                "characteristics": ["Logical", "Goal-oriented", "Self-reliant"],
                "strategies": ["Practice empathy", "Seek balance", "Manage stress"]
            },
            {
                "name": "Avoidant",
                "description": "Avoids challenges, seeking comfort and leisure.",
                "characteristics": ["Comfort-seeking", "Decision-averse"],
                "strategies": ["Foster resilience", "Practice assertiveness"]
            }
        ]

        subscales = [
            {
                "name": "Problem Solving",
                "archetype_name": "Autonomous",
                "definition": "Logical and methodical problem analysis.",
                "interpretation": "Indicates strong cognitive coping.",
                "profile_correlation": {"Autonomous": 0.8, "Avoidant": 0.2}
            },
            {
                "name": "Relaxing Diversions",
                "archetype_name": "Avoidant",
                "definition": "Preference for leisure activities to reduce stress.",
                "interpretation": "Reflects a reliance on immediate comfort.",
                "profile_correlation": {"Avoidant": 0.9, "Autonomous": 0.1}
            }
        ]

        # Add archetypes
        for archetype in archetypes:
            existing = session.query(Archetype).filter_by(name=archetype["name"]).first()
            if not existing:
                new_archetype = Archetype(
                    name=archetype["name"],
                    description=archetype["description"],
                    characteristics=archetype["characteristics"],
                    strategies=archetype["strategies"]
                )
                session.add(new_archetype)

        session.commit()

        # Add subscales
        for subscale in subscales:
            archetype = session.query(Archetype).filter_by(name=subscale["archetype_name"]).first()
            if archetype:
                existing = session.query(Subscale).filter_by(name=subscale["name"]).first()
                if not existing:
                    new_subscale = Subscale(
                        name=subscale["name"],
                        definition=subscale["definition"],
                        interpretation=subscale["interpretation"],
                        profile_correlation=subscale["profile_correlation"],
                        archetype_id=archetype.id
                    )
                    session.add(new_subscale)

        session.commit()
    except Exception as e:
        print(f"Error preloading data: {e}")
    finally:
        session.close()

# Function to create tables explicitly
def create_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(engine)
