from extensions import db
import re

class Company(db.Model):
    __tablename__ = 'companies'
    
    # รหัสบริษัท 8 หลัก ตัวแรกไม่ขึ้นต้นด้วย 0
    company_id = db.Column(db.String(8), primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(300), nullable=False)
    
    # Relationship with jobs
    jobs = db.relationship('Job', backref='company', lazy=True)
    
    def __init__(self, company_id, company_name, contact_email, location):
        if not self.validate_company_id(company_id):
            raise ValueError("Company ID must be 8 digits and not start with 0")
        if not self.validate_email(contact_email):
            raise ValueError("Invalid email format")
            
        self.company_id = company_id
        self.company_name = company_name
        self.contact_email = contact_email
        self.location = location
    
    @staticmethod
    def validate_company_id(company_id):
        """Validate company ID: 8 digits, first digit not 0"""
        if len(company_id) != 8:
            return False
        if not company_id.isdigit():
            return False
        if company_id[0] == '0':
            return False
        return True
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __repr__(self):
        return f'<Company {self.company_name}>'