import sqlalchemy
import math
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.types import Text,Boolean
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship,validates
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine('sqlite:///gs-collection.db')

class Courses(Base):
    __tablename__='courses'
    
    id=Column(Integer,primary_key=True)
    cname=Column(String, nullable=False,unique=True)
    code=Column(String,nullable=False,unique=True)
    seat=Column(Integer,nullable=False)
    
    students=relationship("Students",secondary="student_course",backref="courses")
    
    def __repr__(self):
        return "<Courses(id={},cname='{}',code='{}',seat={})>".format(self.id,self.cname,self.code,self.seat)
    
class Students(Base):
    __tablename__='students'
    
    id=Column(Integer,primary_key=True)
    sname=Column(String,nullable=False,unique=True)
    snumber=Column(String,nullable=False,unique=True)
    smail=Column(String,nullable=False,unique=True)
    
    def __repr__(self):
        return "<Students(id={},sname='{}',snumber='{}',smail='{}')>".format(self.id,self.sname,self.snumber,self.smail)

class StudentCourse(Base):
    __tablename__='student_course'
    
    id=Column(Integer,primary_key=True)
    sname=Column(String,ForeignKey(Students.sname))
    cname=Column(String,ForeignKey(Courses.cname))
    UniqueConstraint(sname,cname)
    
    def __repr__(self):
        return"<StudentCourse(id={},sname='{}',cname='{}')>".format(self.id,self.sname,self.cname)
    
class Grade_record(Base):
    __tablename__='garde_record'
    
    id=Column(Integer,primary_key=True)
    sname=Column(String,ForeignKey(Students.sname),nullable=False)
    cname=Column(String,ForeignKey(Courses.cname),nullable=False)
    grade=Column(Integer,nullable=False)
    
    @validates('grade')
    def grade_is_valid(self,key,grade):
        grade=math.floor(grade)
        if grade<0 or grade>100:
            raise ValueError('Illegal grade!')
        return grade
    
    def __repr__(self):
        return"<Grade_record(id={},sname='{}',cname='{}',grade={})>".format(self.id,self.sname,self.cname,self.grade)

Base.metadata.create_all(engine)

