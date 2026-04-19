from flask import Blueprint,render_template,redirect,url_for,request
from app.models import User,Application,PlacementDrive,Company,Student
from app.extensions import db
from app.utils import admin_required

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/dashboard',methods=['GET'])
@admin_required
def dashboard():
    students=User.query.filter_by(role='student').count()
    company=User.query.filter_by(role='company').count()
    application=Application.query.count()
    placement_drive=PlacementDrive.query.count()
    return render_template('admin/dashboard.html',
                           students=students,
                           company=company,
                           application=application,
                           placement_drives=placement_drive)
@admin_bp.route('/company', methods=['GET'])
@admin_required
def companies():
    search = request.args.get('search', '')
    if search:
        companies = Company.query.join(User, Company.user_id == User.id).filter(
            Company.company_name.ilike(f'%{search}%')
        ).all()
    else:
        companies = Company.query.all()
    return render_template('admin/company.html', companies=companies)
@admin_bp.route('/company/<int:id>/approve',methods=['POST'])
@admin_required
def approve_company(id):
    companies=Company.query.get(id)
    companies.approval_status="Approved"
    db.session.commit()
    return redirect(url_for('admin.companies'))
@admin_bp.route('/company/<int:id>/reject',methods=['POST'])
@admin_required
def reject_company(id):
    companies=Company.query.get(id)
    companies.approval_status="Rejected"
    db.session.commit()
    return redirect(url_for('admin.companies'))
@admin_bp.route('/company/<int:id>/blacklist',methods=['POST'])
@admin_required
def blacklist_company(id):
    companies=Company.query.get(id)
    companies.user.is_active=False
    companies.approval_status='BlackListed'
    db.session.commit()
    return redirect(url_for('admin.companies'))
@admin_bp.route('/company/<int:id>/unblacklist', methods=['POST'])
@admin_required
def unblacklist_company(id):
    company = Company.query.get(id)
    company.user.is_active = True
    company.approval_status = 'Approved'
    db.session.commit()
    return redirect(url_for('admin.companies'))

@admin_bp.route('/students', methods=['GET'])
@admin_required
def students():
    search = request.args.get('search', '')
    if search:
        students = Student.query.join(User, Student.user_id == User.id).filter(
            User.name.ilike(f'%{search}%')
        ).all()
    else:
        students = Student.query.all()
    return render_template('admin/student.html', students=students)
@admin_bp.route('/student/<int:id>/blacklist',methods=['POST'])
@admin_required
def blacklist_student(id):
    student=Student.query.get(id)
    student.user.is_active=False
    db.session.commit()
    return redirect(url_for('admin.students'))
@admin_bp.route('/student/<int:id>/unblacklist', methods=['POST'])
@admin_required
def unblacklist_student(id):
    student = Student.query.get(id)
    student.user.is_active = True
    db.session.commit()
    return redirect(url_for('admin.students'))

@admin_bp.route('/drives',methods=['GET'])
@admin_required
def drives():
    drives=PlacementDrive.query.all()
    return render_template('admin/drives.html',drives=drives)
@admin_bp.route('/drives/<int:id>/approve',methods=['POST'])
@admin_required
def drives_approve(id):
    drives=PlacementDrive.query.get(id)
    drives.status="Approved"
    db.session.commit()
    return redirect(url_for('admin.drives'))
@admin_bp.route('/drives/<int:id>/reject',methods=['POST'])
@admin_required
def drives_reject(id):
    drives=PlacementDrive.query.get(id)
    drives.status='Rejected'
    db.session.commit()
    return redirect(url_for('admin.drives'))