from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base,Courses,Students,StudentCourse,Grade_record

engine = create_engine('sqlite:///gs-collection.db',connect_args={'check_same_thread': False},  echo=True)
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()
@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["user"] =="kin" and request.form["pw"] == "cs591":
            return redirect(url_for('showCourseList'))
        else:
            print("Wrong combination")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/courses/')
def showCourseList():
    courses = session.query(Courses).all()
    return render_template("courselist.html", courses =courses)

@app.route('/courses/new/',methods=['GET','POST'])
def newCourse():
    if request.method == 'POST':
        if request.form['cname'] != "" and request.form['ccode'] != "" and request.form['climit'] !="":
            newCourse = Courses(cname = request.form['cname'], code = request.form['ccode'], seat = request.form['climit'])
            session.add(newCourse)
            session.commit()
            return redirect(url_for('showCourseList'))
        else:
            return redirect(url_for('showCourseList'))
    else:
        return render_template('newCourse.html')

@app.route('/courses/grades/<course_name>',methods=['GET','POST'])
def showCourseDetail(course_name):
    entry = session.query(Grade_record).filter_by(cname =course_name).all()
    return render_template("classinfo.html", u =entry)


# Create a new student and commit the changes in the database
@app.route('/<cname>/new/', methods=['GET', 'POST'])
def newStudent(cname):
    if request.method == 'POST':
        # student table change
        newStudent = Students(sname=request.form['sname'], snumber=request.form['snumber'], smail=request.form['smail'])
        querytest=session.query(Students).filter_by(sname=request.form['sname']).all()
        if querytest is not empty:
            session.add(newStudent)
        # student_course table change
        newStudentCourse = StudentCourse(sname=request.form['sname'], cname='cname')
        session.add(newStudentCourse)
        # grade_record table change
        newGradeRecord = GradeRecord(sname=request.form['sname'], cname='cname', grade=request.form['grade'])
        session.add(newGradeRecord)
        session.commit()
        return redirect(url_for('showcourse'))
    else:
        return render_template('classinfo.html')

@app.route('/<string:cname>/<string:sname>/delete',methods=['GET','POST'])
def deletestudent(sname,cname):
    # student_course table change
    studentcourseToDelete=session.query(StudentCourse).filter(and_(sname=sname,cname=cname)).one()
    # grade_record table change
    graderecordToDelete=session.query(Grade_record).filter(and_(sname=sname,cname=cname)).one()
    if request.method=='POST':
        session.delete(studentcourseToDelete)
        session.delete(graderecordToDelete)
        session.commit()
        return redirect(url_for('showcourse'))
    else:
        return render_template('deletestudent.html')

@app.route('/<string:cname>/<string:sname>/edit',methods=['GET','POST'])
def editstudent(sname,cname):
    # edit student table
    editedStudent=session.query(Students).filter_by(sname=sname).one()
    # edit studentcourse table
    editedStudentCourse=session.query(StudentCourse).filter(and_(sname=sname,cname=cname)).one()
    # edit graderecord table
    editedGradeRecord=session.query(Grade_record).filter(and_(sname=sname,cname=cname)).one()
    if request.method=='POST':
        if sname!=request.form['sname']:
            editedStudent.sname=request.form['sname']
            editedStudent.snumber=request.form['snumber']
            editedStudent.smail=request.form['smail']

            editedStudentCourse.sname=request.form['sname']

            editedGradeRecord.sname=request.form['sname']
            editedGradeRecord.grade=request.form['grade']
            session.commit()
        elif snumber!=request.form['snumber'] or smail!=request.form['smail']:
            editedStudent.snumber = request.form['snumber']
            editedStudent.smail = request.form['smail']
            session.commit()
        elif grade!=request.form['grade']:
            editedGradeRecord.grade=request.form['grade']
            session.commit()
        return redirect(url_for('showcourse'))
    else:
        return render_template('editStudent.html',sname=sname)


if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=4996)




