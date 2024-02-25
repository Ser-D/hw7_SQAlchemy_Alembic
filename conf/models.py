from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__: str = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(75), nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(75), nullable=False)
    teacher_id = Column(ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship("Teacher", backref='disciplines')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    grade_date = Column(Date, nullable=False)
    discipline_id = Column(ForeignKey("disciplines.id", ondelete="CASCADE"))
    discipline = relationship('Discipline', backref='grades')
    student_id = Column(ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grades')
