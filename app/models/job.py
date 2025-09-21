from extensions import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    # รหัสตำแหน่งงาน 8 หลัก ตัวแรกไม่ขึ้นต้นด้วย 0
    job_id = db.Column(db.String(8), primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.String(8), db.ForeignKey('companies.company_id'), nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='เปิด')  # 'เปิด' หรือ 'ปิด'
    job_type = db.Column(db.String(20), nullable=False)  # 'งานปกติ' หรือ 'สหกิจศึกษา'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with applications
    applications = db.relationship('Application', backref='job', lazy=True)
    
    def __init__(self, job_id, job_title, job_description, company_id, application_deadline, job_type, status='เปิด'):
        if not self.validate_job_id(job_id):
            raise ValueError("Job ID must be 8 digits and not start with 0")
        if status not in ['เปิด', 'ปิด']:
            raise ValueError("Status must be 'เปิด' or 'ปิด'")
        if job_type not in ['งานปกติ', 'สหกิจศึกษา']:
            raise ValueError("Job type must be 'งานปกติ' or 'สหกิจศึกษา'")
            
        self.job_id = job_id
        self.job_title = job_title
        self.job_description = job_description
        self.company_id = company_id
        self.application_deadline = application_deadline
        self.status = status
        self.job_type = job_type
    
    @staticmethod
    def validate_job_id(job_id):
        """Validate job ID: 8 digits, first digit not 0"""
        if len(job_id) != 8:
            return False
        if not job_id.isdigit():
            return False
        if job_id[0] == '0':
            return False
        return True
    
    def is_open(self):
        """Check if job is open for applications"""
        return self.status == 'เปิด' and self.application_deadline >= datetime.now().date()
    
    def __repr__(self):
        return f'<Job {self.job_title}>'