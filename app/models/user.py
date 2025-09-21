from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'user', 'company', 'admin'
    
    # Optional foreign keys based on user type
    candidate_id = db.Column(db.String(8), db.ForeignKey('candidates.candidate_id'), nullable=True)
    company_id = db.Column(db.String(8), db.ForeignKey('companies.company_id'), nullable=True)
    
    # Relationships
    candidate = db.relationship('Candidate', backref='user_account', lazy=True)
    company = db.relationship('Company', backref='user_account', lazy=True)
    
    def __init__(self, username, email, password, user_type, candidate_id=None, company_id=None):
        if user_type not in ['user', 'company', 'admin']:
            raise ValueError("User type must be 'user', 'company', or 'admin'")
            
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        self.candidate_id = candidate_id
        self.company_id = company_id
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type == 'admin'
    
    def is_company(self):
        """Check if user is company"""
        return self.user_type == 'company'
    
    def is_regular_user(self):
        """Check if user is regular user"""
        return self.user_type == 'user'
    
    def __repr__(self):
        return f'<User {self.username}>'