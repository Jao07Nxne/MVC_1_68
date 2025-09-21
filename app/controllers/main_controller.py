from flask import Blueprint, render_template, redirect, url_for, request, flash
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

@main_bp.route('/admin/reports')
@login_required
def admin_reports():
    """หน้ารายงานระบบสำหรับ Admin"""
    if not current_user.is_admin():
        return redirect(url_for('main.dashboard'))
    
    from app.models.company import Company
    from app.models.job import Job
    from app.models.candidate import Candidate
    from app.models.application import Application
    from datetime import datetime, timedelta
    
    # สถิติโดยรวม
    total_jobs = Job.query.count()
    total_companies = Company.query.count()
    total_candidates = Candidate.query.count()
    total_applications = Application.query.count()
    
    # สถิติย้อนหลัง 30 วัน
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_jobs = Job.query.filter(Job.created_at >= thirty_days_ago).count()
    recent_applications = Application.query.filter(Application.application_date >= thirty_days_ago).count()
    
    # สถิติตามประเภทงาน
    regular_jobs = Job.query.filter_by(job_type='งานปกติ').count()
    internship_jobs = Job.query.filter_by(job_type='สหกิจศึกษา').count()
    
    # สถิติตามสถานะ
    open_jobs = Job.query.filter_by(status='เปิด').count()
    closed_jobs = Job.query.filter_by(status='ปิด').count()
    
    # สถิติการสมัครตามสถานะ
    pending_applications = Application.query.filter_by(status='รอพิจารณา').count()
    approved_applications = Application.query.filter_by(status='ผ่าน').count()
    rejected_applications = Application.query.filter_by(status='ไม่ผ่าน').count()
    
    # บริษัทที่มีงานมากที่สุด
    top_companies = db.session.query(Company, db.func.count(Job.job_id).label('job_count'))\
        .join(Job).group_by(Company.company_id)\
        .order_by(db.func.count(Job.job_id).desc()).limit(5).all()
    
    report_data = {
        'total_stats': {
            'total_jobs': total_jobs,
            'total_companies': total_companies,
            'total_candidates': total_candidates,
            'total_applications': total_applications,
        },
        'recent_stats': {
            'recent_jobs': recent_jobs,
            'recent_applications': recent_applications,
        },
        'job_type_stats': {
            'regular_jobs': regular_jobs,
            'internship_jobs': internship_jobs,
        },
        'job_status_stats': {
            'open_jobs': open_jobs,
            'closed_jobs': closed_jobs,
        },
        'application_status_stats': {
            'pending': pending_applications,
            'approved': approved_applications,
            'rejected': rejected_applications,
        },
        'top_companies': top_companies
    }
    
    return render_template('admin_reports.html', report_data=report_data)

@main_bp.route('/admin/settings')
@login_required
def admin_settings():
    """หน้าตั้งค่าระบบสำหรับ Admin"""
    if not current_user.is_admin():
        return redirect(url_for('main.dashboard'))
    
    from app.models.company import Company
    from app.models.job import Job
    from app.models.candidate import Candidate
    from app.models.user import User
    
    # ข้อมูลระบบ
    system_info = {
        'version': '1.0.0',
        'database': 'SQLite',
        'total_users': User.query.count(),
        'admin_users': User.query.filter_by(user_type='admin').count(),
        'company_users': User.query.filter_by(user_type='company').count(),
        'regular_users': User.query.filter_by(user_type='user').count(),
    }
    
    return render_template('admin_settings.html', system_info=system_info)

@main_bp.route('/profile')
@login_required
def profile():
    """หน้าแสดงโปรไฟล์ผู้ใช้"""
    return render_template('profile.html', user=current_user)

@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """หน้าแก้ไขโปรไฟล์ผู้ใช้"""
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        status = request.form.get('status', '').strip()
        
        # ตรวจสอบข้อมูล
        if not first_name or not last_name or not email:
            flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
            return render_template('edit_profile.html', user=current_user)
        
        # ตรวจสอบว่าอีเมลซ้ำกับผู้ใช้อื่นหรือไม่
        from app.models.user import User
        existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_user:
            flash('อีเมลนี้ถูกใช้แล้ว กรุณาเลือกอีเมลอื่น', 'error')
            return render_template('edit_profile.html', user=current_user)
        
        try:
            # อัพเดทข้อมูลผู้ใช้
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            
            # อัพเดทสถานะถ้ามี candidate profile
            if current_user.candidate and status:
                current_user.candidate.status = status
            
            db.session.commit()
            flash('อัพเดทโปรไฟล์เรียบร้อยแล้ว', 'success')
            return redirect(url_for('main.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการอัพเดทโปรไฟล์', 'error')
            return render_template('edit_profile.html', user=current_user)
    
    return render_template('edit_profile.html', user=current_user)