from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """หน้าล็อกอิน"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        from app.models.user import User
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'ยินดีต้อนรับ {user.username}!', 'success')
            
            # Redirect ตามประเภทผู้ใช้
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """ออกจากระบบ"""
    logout_user()
    flash('ออกจากระบบเรียบร้อยแล้ว', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """หน้าสมัครสมาชิก (สำหรับผู้ใช้ทั่วไป)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        from app.models.user import User
        
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validation
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('รหัสผ่านไม่ตรงกัน', 'error')
            return render_template('auth/register.html')
        
        # ตรวจสอบว่า username หรือ email ซ้ำหรือไม่
        if User.query.filter_by(username=username).first():
            flash('ชื่อผู้ใช้นี้มีคนใช้แล้ว', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้มีคนใช้แล้ว', 'error')
            return render_template('auth/register.html')
        
        try:
            # สร้าง candidate record ก่อน
            from app.models.candidate import Candidate
            import random
            
            # สร้าง candidate_id ที่ไม่ซ้ำ (8 หลัก)
            while True:
                candidate_id = str(random.randint(10000000, 99999999))
                if not Candidate.query.filter_by(candidate_id=candidate_id).first():
                    break
            
            # แยกชื่อและนามสกุลจากข้อมูลที่กรอก (ถ้าไม่มีให้ใช้ username)
            if first_name and last_name:
                candidate_first_name = first_name.strip()
                candidate_last_name = last_name.strip()
            else:
                full_name = username.split()
                if len(full_name) >= 2:
                    candidate_first_name = full_name[0]
                    candidate_last_name = ' '.join(full_name[1:])
                else:
                    candidate_first_name = username
                    candidate_last_name = 'ผู้ใช้ใหม่'
            
            # สร้าง candidate record
            new_candidate = Candidate(
                candidate_id=candidate_id,
                first_name=candidate_first_name,
                last_name=candidate_last_name,
                email=email,
                status='กำลังศึกษา'  # ค่าเริ่มต้น
            )
            db.session.add(new_candidate)
            db.session.flush()  # เพื่อให้ได้ candidate_id
            
            # สร้างผู้ใช้ใหม่พร้อมเชื่อมโยงกับ candidate
            new_user = User(username, email, password, 'user', candidate_id=candidate_id)
            db.session.add(new_user)
            db.session.commit()
            
            flash('สมัครสมาชิกเรียบร้อยแล้ว กรุณาเข้าสู่ระบบ', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการสมัครสมาชิก', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')