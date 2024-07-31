from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

engine = create_engine("postgresql://postgres:voidpostgres@localhost:5432/eduzonedb", echo=True)

Base = declarative_base()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(70), unique=True)
    password = Column(String(20), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, ForeignKey('role.name'))
    joined_at = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<User(username={self.username})>"
    

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<Role(name={self.name})>"


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Category(category={self.name})>"
    

class Course(Base):
    __tablename__ = 'course'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    description = Column(Text)
    instructor_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    lectures = relationship("Lecture", back_populates='lecture') # One to Many relationship

    def __repr__(self):
        return f"<Course(title={self.title})>"


class Lecture(Base):
    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    title = Column(String(150))
    description = Column(Text)
    order_index = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    contents = relationship("Content", back_populates='content')

    def __repr__(self):
        return f"<Lecture(title={self.title})>"


class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('lecture.id'))
    file_path = Column(String, nullable=False)
    content_type = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Content(file_path={self.file_path})>"


class Enrollment(Base):
    __tablename__ = 'enrollment'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    enrolled_at = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Enrollment(user_id={self.user_id}, course_id={self.course_id})>"


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")