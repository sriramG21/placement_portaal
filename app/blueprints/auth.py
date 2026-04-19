from flask import Blueprint,render_template,request,url_for,redirect,flash
from app.models import User,Student,Company
from werkzeug.security import generate_password_hash,check_password_hash
from app.extensions import db
from flask_login import login_user,logout_user
auth_bp=Blueprint('auth',__name__)
@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/register',methods=["GET","POST"])
def register():
    if (request.method=='POST'):
        role=request.form.get('role')
        if(role=='student'):
           return redirect(url_for('auth.register_student'))
        else:
            return redirect(url_for('auth.register_company'))
    return render_template('auth/register.html')


@auth_bp.route('/register/student',methods=['GET','POST'])
def register_student():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        roll_no=request.form.get('roll_no')
        cgpa=float(request.form.get('cgpa'))
        department=request.form.get('department')
        
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'danger')
            return render_template('auth/register_student.html')
        # check duplicate roll_no
        existing_roll = Student.query.filter_by(roll_no=roll_no).first()
        if existing_roll:
            flash('Roll number already registered!', 'danger')
            return render_template('auth/register_student.html')
        hashed_password=generate_password_hash(password)
        user=User(
            name=name,
                  email=email,
                  password=hashed_password,
                  role='student'
                  )
        db.session.add(user)
        db.session.commit()
        
        student=Student(user_id=user.id,
            roll_no=roll_no,
                        cgpa=cgpa,
                        department=department)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register_student.html')
    
@auth_bp.route('/register/company',methods=['GET','POST'])
def register_company():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        company_name=request.form.get('company_name')
        hr_contact=request.form.get('hr_contact')
        website=request.form.get('website')
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'danger')
            return render_template('auth/register_company.html')
        hashed_password=generate_password_hash(password)
        user=User(name=name,
                  email=email,
                  password=hashed_password,
                  role='company'
                  )
        db.session.add(user)
        db.session.commit()
        company=Company(user_id=user.id,company_name=company_name,
                  hr_contact=hr_contact,
                  website=website)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register_company.html')
@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password,password):
                flash('Invalid email or password', 'danger')
                return render_template('auth/login.html')
        if not user.is_active:
            flash('The account got blocked,contact the authority!', 'danger')
            return render_template('auth/login.html')
        login_user(user)
        if(user.role=='student'):
            return redirect(url_for('student.dashboard'))
        elif(user.role=='admin'):
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('company.dashboard'))
    return render_template('auth/login.html')
@auth_bp.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))