from extensions import db
import re

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    # รหัสผู้สมัคร 8 หลัก ตัวแรกไม่ขึ้นต้นด้วย 0
    candidate_id = db.Column(db.String(8), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False)  # 'กำลังศึกษา' หรือ 'จบแล้ว'
    
    # Relationship with applications
    applications = db.relationship('Application', backref='candidate', lazy=True)
    
    def __init__(self, candidate_id, first_name, last_name, email, status):
        if not self.validate_candidate_id(candidate_id):
            raise ValueError("Candidate ID must be 8 digits and not start with 0")
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        if status not in ['กำลังศึกษา', 'จบแล้ว']:
            raise ValueError("Status must be 'กำลังศึกษา' or 'จบแล้ว'")
            
        self.candidate_id = candidate_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.status = status
    
    @staticmethod
    def validate_candidate_id(candidate_id):
        """Validate candidate ID: 8 digits, first digit not 0"""
        if len(candidate_id) != 8:
            return False
        if not candidate_id.isdigit():
            return False
        if candidate_id[0] == '0':
            return False
        return True
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @property
    def full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}"
    
    def can_apply_for_internship(self):
        """Check if candidate can apply for internship (only students)"""
        return self.status == 'กำลังศึกษา'
    
    def can_apply_for_regular_job(self):
        """Check if candidate can apply for regular job (only graduates)"""
        return self.status == 'จบแล้ว'
    
    def __repr__(self):
        return f'<Candidate {self.full_name}>'