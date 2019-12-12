from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from dbsetup import Courses,Students,StudentCourse, Grade_record,Base

engine = create_engine('sqlite:///:memory:',connect_args={'check_same_thread': False},  echo=True)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["user"] =="kin" and request.form["pw"] == "cs591":
            return redirect(url_for('showCourseList'))
    else:
        return render_template('login.html')
        
@app.route('/courses')
def showCourseList():
    courses = session.query(Courses).all()
    return render_template("courselist.html", courses =courses)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4966)