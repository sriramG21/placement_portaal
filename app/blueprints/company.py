from flask import Blueprint,render_template,request,redirect,url_for,flash
from app.models import PlacementDrive,Company,Application
from app.extensions import db
from flask_login import current_user,login_required
from  datetime import datetime
from app.utils import company_required
import os


company_bp=Blueprint('company',__name__)
@company_bp.route('/dashboard',methods=['GET'])
@company_required
def dashboard():
    
    drives=PlacementDrive.query.filter_by(company_id=current_user.company.id).all()
    return render_template('company/dashboard.html',drives=drives)
@company_bp.route("/create_drive", methods=["GET", "POST"])
@company_required
def create_drive():
    if current_user.company.approval_status != "Approved":
        flash('Still your company is not approved by the admin!', 'danger')
        return render_template('company/dashboard.html')
    if request.method == "POST":
        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")
        eligibility = request.form.get("eligibility_criteria")
        deadline = datetime.strptime(request.form['application_deadline'], '%Y-%m-%d')
        drive = PlacementDrive(
            company_id=current_user.company.id,
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility,
            application_deadline=deadline,
            status="Pending"
        )
        db.session.add(drive)
        file = request.files.get('jd_pdf')
        if file:
            filename = file.filename
            file.save(os.path.join('app/static/uploads/jd_pdf', filename))
            drive.jd_pdf = filename
        db.session.commit()
        return redirect(url_for("company.dashboard"))
    return render_template("company/create_drive.html")
@company_bp.route('/drive/<int:id>/applicants',methods=['GET'])
@company_required
def application(id):
    applications=Application.query.filter_by(drive_id=id).all()
    return render_template('company/applicants.html',applications=applications)
@company_bp.route('/applications/<int:id>/select',methods=['POST'])
@company_required
def select_application(id):
    application=Application.query.get(id)
    application.status="Selected"
    db.session.commit()
    return redirect(url_for('company.application',id=application.drive_id))
@company_bp.route('/applications/<int:id>/reject',methods=['POST'])
@company_required
def reject_application(id):
    application=Application.query.get(id)
    application.status="Rejected"
    db.session.commit()
    return redirect(url_for('company.application',id=application.drive_id))
@company_bp.route('/applications/<int:id>/shortlist', methods=['POST'])
@company_required
def shortlist_application(id):
    application = Application.query.get(id)
    application.status = 'Shortlisted'
    db.session.commit()
    return redirect(url_for('company.application', id=application.drive_id))