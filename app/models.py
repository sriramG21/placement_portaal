from app.extensions import db,login_manager
from flask_login import UserMixin
from datetime import datetime
class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Company(db.Model):
    __tablename__='companies'
    id=db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    company_name=db.Column(db.String(100),nullable=False)
    hr_contact=db.Column(db.String(100),nullable=False)
    website=db.Column(db.String(200),nullable=False)
    approval_status=db.Column(db.String(20),default='Pending')
    user = db.relationship('User', backref=db.backref('company', uselist=False))
class Student(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    roll_no=db.Column(db.String(30),unique=True,nullable=False)
    cgpa=db.Column(db.Float,nullable=False)
    department=db.Column(db.String(100),nullable=False)
    resume=db.Column(db.String(200),nullable=True)
    user = db.relationship('User', backref=db.backref('student',uselist=False))
class PlacementDrive(db.Model):
    __tablename__='placement_drives'
    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey('companies.id'))
    job_title=db.Column(db.String(100),nullable=False)
    job_description=db.Column(db.Text,nullable=False)
    eligibility_criteria=db.Column(db.Text,nullable=False)
    application_deadline=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(20),default='Pending')
    jd_pdf = db.Column(db.String(200), nullable=True)
    company = db.relationship('Company', backref='drives')
class Application(db.Model):
    __tablename__='applications'
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('students.id'))
    drive_id=db.Column(db.Integer,db.ForeignKey('placement_drives.id'))
    application_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(20),default='Applied')
    drive = db.relationship('PlacementDrive', backref='applications')
    student = db.relationship('Student', backref='student_applications')
    