from extensions import db
from datetime import datetime, timezone, timedelta

# เขตเวลาประเทศไทย (UTC+7)
THAILAND_TZ = timezone(timedelta(hours=7))

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.String(8), db.ForeignKey('candidates.candidate_id'), nullable=False)
    job_id = db.Column(db.String(8), db.ForeignKey('jobs.job_id'), nullable=False)
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(THAILAND_TZ), nullable=False)
    status = db.Column(db.String(20), default='รอพิจารณา', nullable=False)  # 'รอพิจารณา', 'ผ่าน', 'ไม่ผ่าน'
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (db.UniqueConstraint('candidate_id', 'job_id', name='unique_application'),)
    
    def __init__(self, candidate_id, job_id):
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.application_date = datetime.now(THAILAND_TZ)
        self.status = 'รอพิจารณา'
    
    def __repr__(self):
        return f'<Application {self.candidate_id} -> {self.job_id}>'


class InternshipApplicationModel:
    """Model สำหรับการสมัครตำแหน่งสหกิจศึกษา - รับเฉพาะผู้สมัครที่มีสถานะ 'กำลังศึกษา'"""
    
    @staticmethod
    def can_apply(candidate, job):
        """ตรวจสอบว่าผู้สมัครสามารถสมัครสหกิจศึกษาได้หรือไม่"""
        if job.job_type != 'สหกิจศึกษา':
            return False, "ตำแหน่งนี้ไม่ใช่สหกิจศึกษา"
        
        if candidate.status != 'กำลังศึกษา':
            return False, "สหกิจศึกษารับเฉพาะผู้ที่มีสถานะ 'กำลังศึกษา' เท่านั้น"
        
        if not job.is_open():
            return False, "ตำแหน่งนี้ปิดรับสมัครแล้ว"
        
        # ตรวจสอบว่าเคยสมัครแล้วหรือไม่
        existing_application = Application.query.filter_by(
            candidate_id=candidate.candidate_id,
            job_id=job.job_id
        ).first()
        
        if existing_application:
            return False, "คุณได้สมัครตำแหน่งนี้แล้ว"
        
        return True, "สามารถสมัครได้"
    
    @staticmethod
    def apply(candidate, job):
        """สมัครสหกิจศึกษา"""
        can_apply, message = InternshipApplicationModel.can_apply(candidate, job)
        
        if not can_apply:
            raise ValueError(message)
        
        application = Application(candidate.candidate_id, job.job_id)
        db.session.add(application)
        db.session.commit()
        
        return application


class RegularJobApplicationModel:
    """Model สำหรับการสมัครตำแหน่งปกติ - รับเฉพาะผู้สมัครที่มีสถานะ 'จบแล้ว'"""
    
    @staticmethod
    def can_apply(candidate, job):
        """ตรวจสอบว่าผู้สมัครสามารถสมัครงานปกติได้หรือไม่"""
        if job.job_type != 'งานปกติ':
            return False, "ตำแหน่งนี้ไม่ใช่งานปกติ"
        
        if candidate.status != 'จบแล้ว':
            return False, "งานปกติรับเฉพาะผู้ที่มีสถานะ 'จบแล้ว' เท่านั้น"
        
        if not job.is_open():
            return False, "ตำแหน่งนี้ปิดรับสมัครแล้ว"
        
        # ตรวจสอบว่าเคยสมัครแล้วหรือไม่
        existing_application = Application.query.filter_by(
            candidate_id=candidate.candidate_id,
            job_id=job.job_id
        ).first()
        
        if existing_application:
            return False, "คุณได้สมัครตำแหน่งนี้แล้ว"
        
        return True, "สามารถสมัครได้"
    
    @staticmethod
    def apply(candidate, job):
        """สมัครงานปกติ"""
        can_apply, message = RegularJobApplicationModel.can_apply(candidate, job)
        
        if not can_apply:
            raise ValueError(message)
        
        application = Application(candidate.candidate_id, job.job_id)
        db.session.add(application)
        db.session.commit()
        
        return application