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
        if request.form["user"] =="kinan" and request.form["pw"] == "cs591":
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

@app.route('/courses/<course_name>/')
def showCourseDetail(course_name):
    entry = session.query(Grade_record).filter_by(cname =course_name).all()
    return render_template("classinfo.html", u = entry, classes = course_name)


# Create a new student and commit the changes in the database
@app.route('/courses/<course_name>/news/', methods=['GET', 'POST'])
def newStudent(course_name):
    if request.method == 'POST':
        if request.form['sname'] != "" and request.form['sid'] != "" and request.form['semail'] !="":
            # student table change
            form_sname = request.form['sname']
            newStudent = Students(sname=form_sname, snumber=request.form['sid'], smail=request.form['semail'])
            querytest=session.query(Students).filter_by(sname=form_sname).all()
            if not querytest:
                session.add(newStudent)
            # student_course table change
            newStudentCourse = StudentCourse(sname=form_sname, cname=course_name)
            session.add(newStudentCourse)
            # grade_record table change
            newGradeRecord = Grade_record(sname=form_sname, cname = course_name, grade=int(request.form['sgrade']))
            session.add(newGradeRecord)
            session.commit()
            return redirect(url_for('showCourseDetail', course_name = course_name))
        else:
            return render_template('newStudent.html', course_name = course_name)
    else:
        return render_template('newStudent.html', course_name = course_name)

@app.route('/courses/<cname>/<sname>/delete',methods=['GET','POST'])
def deleteStudent(sname,cname):
    # edit student table
    editedStudent=session.query(Students).filter_by(sname=sname).one()
    # student_course table change
    studentcourseToDelete=session.query(StudentCourse).filter_by(sname=sname,cname=cname).one()
    # grade_record table change
    graderecordToDelete=session.query(Grade_record).filter_by(sname=sname,cname=cname).one()
    if request.method=='POST':
        if request.form["buttons"] == "delete":
            session.delete(studentcourseToDelete)
            session.delete(graderecordToDelete)
            session.commit()
        return redirect(url_for('showCourseDetail', course_name = cname))
    else:
        return render_template('deleteStudent.html',student = editedStudent, grades = graderecordToDelete, cname= cname)

@app.route('/courses/<cname>/<sname>/edit',methods=['GET','POST'])
def editStudent(sname,cname):
    # edit student table
    editedStudent=session.query(Students).filter_by(sname=sname).one()
    # edit studentcourse table
    editedStudentCourse=session.query(StudentCourse).filter_by(sname=sname,cname=cname).one()
    # edit graderecord table
    editedGradeRecord=session.query(Grade_record).filter_by(sname=sname,cname=cname).one()
    if request.method=='POST':
        if request.form['sname'] or request.form['sid'] or request.form['semail'] or request.form['sgrade']:
            editedStudent.sname=request.form['sname']
            editedStudent.snumber=request.form['sid']
            editedStudent.smail=request.form['semail']

            editedStudentCourse.sname=request.form['sname']

            editedGradeRecord.sname=request.form['sname']
            editedGradeRecord.grade=int(request.form['sgrade'])
            session.commit()
        return redirect(url_for('showCourseDetail', course_name = cname))
    else:
        return render_template('editStudent.html',student = editedStudent, grades = editedGradeRecord, cname= cname)


if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=4996)




