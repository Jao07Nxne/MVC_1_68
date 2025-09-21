from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """หน้าแรก - แสดงตำแหน่งงานที่เปิด"""
    from app.models.job import Job
    
    # ดึงตำแหน่งงานที่เปิดเท่านั้น และเรียงลำดับ
    open_jobs = Job.query.filter_by(status='เปิด').order_by(
        Job.job_type.asc(),  # เรียงตามประเภทงาน (งานปกติ ก่อน สหกิจศึกษา)
        Job.application_deadline.asc(),  # เรียงตามวันสุดท้าย
        Job.job_title.asc()  # เรียงตามชื่อตำแหน่ง
    ).all()
    
    # กรองเฉพาะงานที่ยังไม่หมดเขต
    current_open_jobs = [job for job in open_jobs if job.is_open()]
    
    # ส่ง today สำหรับใช้ในการคำนวณวันคงเหลือ
    thailand_tz = datetime.now().astimezone().tzinfo
    today = datetime.now(thailand_tz).date()
    
    return render_template('index.html', jobs=current_open_jobs, today=today)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """หน้า Dashboard สำหรับผู้ใช้ที่ล็อกอินแล้ว"""
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.is_company():
        return redirect(url_for('main.company_dashboard'))
    else:
        return redirect(url_for('main.user_dashboard'))

@main_bp.route('/user_dashboard')
@login_required
def user_dashboard():
    """Dashboard สำหรับผู้ใช้ทั่วไป"""
    if not current_user.is_regular_user():
        return redirect(url_for('main.dashboard'))
    
    # ดึงใบสมัครของผู้ใช้
    applications = []
    if current_user.candidate:
        from app.models.application import Application
        
        candidate = current_user.candidate
        applications = Application.query.filter_by(candidate_id=candidate.candidate_id).order_by(
            Application.application_date.desc()
        ).all()
    
    return render_template('user_dashboard.html', applications=applications)

@main_bp.route('/company_dashboard')
@login_required
def company_dashboard():
    """Dashboard สำหรับบริษัท"""
    if not current_user.is_company():
        return redirect(url_for('main.dashboard'))
    
    from app.models.job import Job
    
    # ดึงตำแหน่งงานของบริษัท
    company_jobs = Job.query.filter_by(company_id=current_user.company_id).all()
    
    return render_template('company_dashboard.html', jobs=company_jobs)

@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    """Dashboard สำหรับ Admin"""
    if not current_user.is_admin():
        return redirect(url_for('main.dashboard'))
    
    from app.models.job import Job
    from app.models.company import Company
    from app.models.candidate import Candidate
    from app.models.application import Application
    
    # สถิติระบบ
    total_jobs = Job.query.count()
    total_companies = Company.query.count()
    total_candidates = Candidate.query.count()
    total_applications = Application.query.count()
    
    stats = {
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_candidates': total_candidates,
        'total_applications': total_applications,
        'open_jobs': Job.query.filter_by(status='เปิด').count()
    }
    
    return render_template('admin_dashboard.html', stats=stats)