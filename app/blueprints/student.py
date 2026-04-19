from flask import Blueprint,render_template,request,redirect,url_for,flash
from app.models import PlacementDrive,Company,Application,Student
from app.extensions import db
from flask_login import current_user,login_required
from  datetime import datetime
import os
from app.utils import student_required


student_bp=Blueprint('student',__name__)


@student_bp.route('/dashboard',methods=['GET'])
@student_required
def dashboard():
    application_count = Application.query.filter_by(
        student_id=current_user.student.id
    ).count()
    return render_template('student/dashboard.html',
                           application_count=application_count)
@student_bp.route('/drives', methods=['GET'])
@student_required
def drives():
    drives = PlacementDrive.query.filter_by(status='Approved').all()
    applications = Application.query.filter_by(
        student_id=current_user.student.id
    ).all()
    return render_template('student/drives.html', 
                           drives=drives, 
                           applications=applications)
@student_bp.route('/drives/<int:id>/apply' ,methods=['POST'])
@student_required
def apply(id):
    existing=Application.query.filter_by(student_id=current_user.student.id,drive_id=id).first()
    if existing:
        flash('you already applied', 'danger')
        return render_template('student/drives.html')
    application = Application(
    student_id=current_user.student.id,
    drive_id=id,
    status='Applied'
    )
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('student.dashboard'))
@student_bp.route('/application',methods=['GET'])
@student_required
def application():
    applications=Application.query.filter_by(student_id=current_user.student.id).all()
    return render_template('student/applications.html',applications=applications)
@student_bp.route('/profile',methods=['GET','POST'])
@student_required
def profile():
    if request.method=='POST':
        name=request.form.get('name')
        cgpa=float(request.form.get('cgpa'))
        roll_no=request.form.get('roll_no')
        current_user.name=name
        current_user.student.cgpa=cgpa
        current_user.student.roll_no=roll_no
        file = request.files.get('resume')
        if file:
            filename = file.filename
            file.save(os.path.join('app/static/uploads/resumes', filename))
            current_user.student.resume = filename
        db.session.commit()
        return redirect(url_for('student.dashboard'))
    return render_template('student/profile.html')
   