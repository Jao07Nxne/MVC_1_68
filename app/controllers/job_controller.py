from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/')
def list_jobs():
    """แสดงรายการตำแหน่งงานที่เปิด"""
    from app.models.job import Job
    
    # กรองตามประเภทงาน
    job_type = request.args.get('type', 'all')
    
    query = Job.query.filter_by(status='เปิด')
    
    if job_type == 'regular':
        query = query.filter_by(job_type='งานปกติ')
    elif job_type == 'internship':
        query = query.filter_by(job_type='สหกิจศึกษา')
    
    # เรียงลำดับ
    jobs = query.order_by(
        Job.job_type.asc(),
        Job.application_deadline.asc(),
        Job.job_title.asc()
    ).all()
    
    # กรองเฉพาะงานที่ยังไม่หมดเขต
    current_open_jobs = [job for job in jobs if job.is_open()]
    
    # ส่ง today สำหรับใช้ในการคำนวณวันคงเหลือ
    thailand_tz = datetime.now().astimezone().tzinfo
    today = datetime.now(thailand_tz).date()
    
    return render_template('jobs/list.html', jobs=current_open_jobs, job_type=job_type, today=today)

@job_bp.route('/<job_id>')
def job_detail(job_id):
    """แสดงรายละเอียดตำแหน่งงาน"""
    from app.models.job import Job
    from app.models.application import InternshipApplicationModel, RegularJobApplicationModel
    
    job = Job.query.get_or_404(job_id)
    
    # ตรวจสอบว่าผู้ใช้สามารถสมัครได้หรือไม่
    can_apply = False
    apply_message = ""
    
    if current_user.is_authenticated and current_user.candidate:
        candidate = current_user.candidate
        
        if job.job_type == 'สหกิจศึกษา':
            can_apply, apply_message = InternshipApplicationModel.can_apply(candidate, job)
        elif job.job_type == 'งานปกติ':
            can_apply, apply_message = RegularJobApplicationModel.can_apply(candidate, job)
    
    # ส่ง today สำหรับใช้ในการคำนวณวันคงเหลือ
    thailand_tz = datetime.now().astimezone().tzinfo
    today = datetime.now(thailand_tz).date()
    
    return render_template('jobs/detail.html', job=job, can_apply=can_apply, apply_message=apply_message, today=today)

@job_bp.route('/<job_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    """หน้าสมัครงาน"""
    from app.models.job import Job
    from app.models.application import InternshipApplicationModel, RegularJobApplicationModel
    
    job = Job.query.get_or_404(job_id)
    
    # ตรวจสอบว่าผู้ใช้มี candidate หรือไม่
    if not current_user.candidate:
        # สร้าง candidate record อัตโนมัติสำหรับผู้ใช้เก่า
        try:
            from app.models.candidate import Candidate
            import random
            
            # สร้าง candidate_id ที่ไม่ซ้ำ (8 หลัก)
            while True:
                candidate_id = str(random.randint(10000000, 99999999))
                if not Candidate.query.filter_by(candidate_id=candidate_id).first():
                    break
            
            # สร้าง candidate record ด้วยข้อมูลพื้นฐาน
            new_candidate = Candidate(
                candidate_id=candidate_id,
                first_name=current_user.username,
                last_name='ผู้ใช้',
                email=current_user.email,
                status='กำลังศึกษา'
            )
            db.session.add(new_candidate)
            
            # อัปเดต user record เพื่อเชื่อมโยงกับ candidate
            current_user.candidate_id = candidate_id
            db.session.commit()
            
            flash('ระบบได้สร้างโปรไฟล์ผู้สมัครงานให้คุณอัตโนมัติ คุณสามารถแก้ไขข้อมูลได้ในหน้า Dashboard', 'info')
            
        except Exception as e:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการสร้างโปรไฟล์ผู้สมัครงาน กรุณาลองใหม่อีกครั้ง', 'error')
            return redirect(url_for('jobs.job_detail', job_id=job_id))
    
    # หลังจากตรวจสอบแล้ว ตอนนี้ user ควรมี candidate record แล้ว
    candidate = current_user.candidate
    if not candidate:
        flash('เกิดข้อผิดพลาดในการเข้าถึงข้อมูลผู้สมัคร กรุณาลองใหม่อีกครั้ง', 'error')
        return redirect(url_for('jobs.job_detail', job_id=job_id))
    
    if request.method == 'POST':
        try:
            # เลือก Model ตามประเภทงาน
            if job.job_type == 'สหกิจศึกษา':
                application = InternshipApplicationModel.apply(candidate, job)
            elif job.job_type == 'งานปกติ':
                application = RegularJobApplicationModel.apply(candidate, job)
            else:
                flash('ประเภทงานไม่ถูกต้อง', 'error')
                return redirect(url_for('jobs.job_detail', job_id=job_id))
            
            flash(f'สมัครตำแหน่ง "{job.job_title}" เรียบร้อยแล้ว!', 'success')
            
            # Business Rule: กลับไปหน้าตำแหน่งงาน
            return redirect(url_for('jobs.list_jobs'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('jobs.job_detail', job_id=job_id))
        except Exception as e:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการสมัครงาน', 'error')
            return redirect(url_for('jobs.job_detail', job_id=job_id))
    
    # ตรวจสอบความสามารถในการสมัคร
    if job.job_type == 'สหกิจศึกษา':
        can_apply, apply_message = InternshipApplicationModel.can_apply(candidate, job)
    elif job.job_type == 'งานปกติ':
        can_apply, apply_message = RegularJobApplicationModel.can_apply(candidate, job)
    else:
        can_apply, apply_message = False, "ประเภทงานไม่ถูกต้อง"
    
    if not can_apply:
        flash(apply_message, 'error')
        return redirect(url_for('jobs.job_detail', job_id=job_id))
    
    # ดึงเวลาจากเครื่องเพื่อลงวันที่สมัคร
    current_time = datetime.now()
    
    return render_template('jobs/apply.html', job=job, candidate=candidate, current_time=current_time)

@job_bp.route('/api/check_eligibility/<job_id>')
@login_required
def check_eligibility(job_id):
    """API สำหรับตรวจสอบสิทธิ์การสมัครงาน"""
    from app.models.job import Job
    from app.models.application import InternshipApplicationModel, RegularJobApplicationModel
    
    job = Job.query.get_or_404(job_id)
    
    if not current_user.candidate:
        return jsonify({
            'can_apply': False,
            'message': 'คุณต้องเป็นผู้สมัครงานเพื่อใช้ฟีเจอร์นี้'
        })
    
    candidate = current_user.candidate
    
    if job.job_type == 'สหกิจศึกษา':
        can_apply, message = InternshipApplicationModel.can_apply(candidate, job)
    elif job.job_type == 'งานปกติ':
        can_apply, message = RegularJobApplicationModel.can_apply(candidate, job)
    else:
        can_apply, message = False, "ประเภทงานไม่ถูกต้อง"
    
    return jsonify({
        'can_apply': can_apply,
        'message': message,
        'candidate_status': candidate.status,
        'job_type': job.job_type
    })

@job_bp.route('/my_applications')
@login_required
def my_applications():
    """แสดงใบสมัครทั้งหมดของผู้ใช้"""
    from app.models.application import Application
    
    if not current_user.candidate:
        flash('คุณต้องเป็นผู้สมัครงานเพื่อใช้ฟีเจอร์นี้', 'error')
        return redirect(url_for('main.index'))
    
    candidate = current_user.candidate
    applications = Application.query.filter_by(candidate_id=candidate.candidate_id).order_by(
        Application.application_date.desc()
    ).all()
    
    return render_template('jobs/my_applications.html', applications=applications)

@job_bp.route('/company_applications')
@login_required
def company_applications():
    """แสดงรายการผู้สมัครงานทั้งหมดของบริษัท (สำหรับ HR)"""
    from app.models.application import Application
    from app.models.job import Job
    
    if not current_user.is_company() or not current_user.company:
        flash('คุณต้องเป็น HR ของบริษัทเพื่อใช้ฟีเจอร์นี้', 'error')
        return redirect(url_for('main.index'))
    
    company = current_user.company
    
    # ดึงรายการใบสมัครทั้งหมดของบริษัท
    applications = db.session.query(Application).join(Job).filter(
        Job.company_id == company.company_id
    ).order_by(Application.application_date.desc()).all()
    
    return render_template('jobs/company_applications.html', 
                         applications=applications, 
                         company=company)

@job_bp.route('/application/<int:application_id>')
@login_required
def application_detail(application_id):
    """แสดงรายละเอียดใบสมัครแต่ละคน (สำหรับ HR)"""
    from app.models.application import Application
    
    application = Application.query.get_or_404(application_id)
    
    # ตรวจสอบว่า HR มีสิทธิ์ดูใบสมัครนี้หรือไม่
    if not current_user.is_company() or not current_user.company:
        flash('คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้', 'error')
        return redirect(url_for('main.index'))
    
    if application.job.company_id != current_user.company.company_id:
        flash('คุณไม่มีสิทธิ์ดูใบสมัครนี้', 'error')
        return redirect(url_for('jobs.company_applications'))
    
    return render_template('jobs/application_detail.html', application=application)

@job_bp.route('/update_application_status/<int:application_id>', methods=['POST'])
@login_required
def update_application_status(application_id):
    """อัปเดตสถานะใบสมัคร (สำหรับ HR)"""
    from app.models.application import Application
    
    application = Application.query.get_or_404(application_id)
    
    # ตรวจสอบสิทธิ์
    if not current_user.is_company() or not current_user.company:
        flash('คุณไม่มีสิทธิ์ทำการนี้', 'error')
        return redirect(url_for('main.index'))
    
    if application.job.company_id != current_user.company.company_id:
        flash('คุณไม่มีสิทธิ์แก้ไขใบสมัครนี้', 'error')
        return redirect(url_for('jobs.company_applications'))
    
    new_status = request.form.get('status')
    
    if new_status in ['รอพิจารณา', 'ผ่าน', 'ไม่ผ่าน']:
        application.status = new_status
        db.session.commit()
        flash(f'อัปเดตสถานะใบสมัครเป็น "{new_status}" เรียบร้อยแล้ว', 'success')
    else:
        flash('สถานะไม่ถูกต้อง', 'error')
    
    return redirect(url_for('jobs.application_detail', application_id=application_id))