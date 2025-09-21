from extensions import db
from datetime import datetime, timedelta, timezone

# เขตเวลาประเทศไทย (UTC+7)
THAILAND_TZ = timezone(timedelta(hours=7))

def seed_all_data():
    """Seed database with sample data"""
    
    # Import models here to avoid circular imports
    from app.models.company import Company
    from app.models.job import Job
    from app.models.candidate import Candidate
    from app.models.user import User
    
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Seed companies (≥2 บริษัท)
    companies = [
        Company('12345678', 'บริษัท เทคโนโลยี จำกัด', 'hr@tech-company.co.th', 'กรุงเทพมหานคร'),
        Company('23456789', 'บริษัท การเงิน จำกัด (มหาชน)', 'recruit@finance-corp.co.th', 'เชียงใหม่'),
        Company('34567890', 'บริษัท การตลาดดิจิทัล จำกัด', 'jobs@digital-marketing.co.th', 'ขอนแก่น'),
    ]
    
    for company in companies:
        db.session.add(company)
    
    # Seed candidates (≥10 คน)
    candidates = [
        Candidate('11111111', 'สมชาย', 'ใจดี', 'somchai@email.com', 'กำลังศึกษา'),
        Candidate('22222222', 'สุภาพร', 'สวยงาม', 'supaporn@email.com', 'จบแล้ว'),
        Candidate('33333333', 'วิชัย', 'เก่งมาก', 'wichai@email.com', 'กำลังศึกษา'),
        Candidate('44444444', 'มาลี', 'รักงาน', 'malee@email.com', 'จบแล้ว'),
        Candidate('55555555', 'ธนา', 'ขยันดี', 'thana@email.com', 'กำลังศึกษา'),
        Candidate('66666666', 'นิรนาม', 'มั่นใจ', 'nirnam@email.com', 'จบแล้ว'),
        Candidate('77777777', 'ปิยะ', 'สุขใส', 'piya@email.com', 'กำลังศึกษา'),
        Candidate('88888888', 'รัตนา', 'เฉลียวฉลาด', 'ratana@email.com', 'จบแล้ว'),
        Candidate('99999999', 'กิตติ', 'มุ่งมั่น', 'kitti@email.com', 'กำลังศึกษา'),
        Candidate('12121212', 'ศิริ', 'ประสบความสำเร็จ', 'siri@email.com', 'จบแล้ว'),
        Candidate('13131313', 'วิภา', 'กล้าหาญ', 'wipa@email.com', 'กำลังศึกษา'),
        Candidate('14141414', 'อนันต์', 'มีความสุข', 'anan@email.com', 'จบแล้ว'),
    ]
    
    for candidate in candidates:
        db.session.add(candidate)
    
    # Commit companies and candidates first
    db.session.commit()
    
    # Seed jobs (≥10 ตำแหน่ง ครอบคลุม ≥2 บริษัท)
    future_date = datetime.now().date() + timedelta(days=30)
    past_date = datetime.now().date() - timedelta(days=5)
    
    jobs = [
        # บริษัท เทคโนโลยี จำกัด
        Job('10000001', 'นักพัฒนาระบบ Senior', 'พัฒนาระบบด้วย Python และ JavaScript มีประสบการณ์ 3+ ปี', '12345678', future_date, 'งานปกติ', 'เปิด'),
        Job('10000002', 'สหกิจศึกษา - Web Developer', 'เรียนรู้การพัฒนาเว็บไซต์ร่วมกับทีมงาน', '12345678', future_date, 'สหกิจศึกษา', 'เปิด'),
        Job('10000003', 'Data Scientist', 'วิเคราะห์ข้อมูลขนาดใหญ่ เชี่ยวชาญ Machine Learning', '12345678', future_date, 'งานปกติ', 'เปิด'),
        Job('10000004', 'สหกิจศึกษา - Data Analyst', 'เรียนรู้การวิเคราะห์ข้อมูลเบื้องต้น', '12345678', future_date, 'สหกิจศึกษา', 'เปิด'),
        Job('10000005', 'DevOps Engineer', 'จัดการระบบ CI/CD และ Cloud Infrastructure', '12345678', future_date, 'งานปกติ', 'เปิด'),
        
        # บริษัท การเงิน จำกัด (มหาชน)
        Job('20000001', 'Financial Analyst', 'วิเคราะห์การลงทุนและความเสี่ยงทางการเงิน', '23456789', future_date, 'งานปกติ', 'เปิด'),
        Job('20000002', 'สหกิจศึกษา - Banking Operations', 'เรียนรู้งานด้านการธนาคาร', '23456789', future_date, 'สหกิจศึกษา', 'เปิด'),
        Job('20000003', 'Risk Management Specialist', 'บริหารความเสี่ยงด้านการเงิน', '23456789', future_date, 'งานปกติ', 'เปิด'),
        Job('20000004', 'Investment Consultant', 'ให้คำปรึกษาการลงทุนแก่ลูกค้า', '23456789', past_date, 'งานปกติ', 'ปิด'),
        
        # บริษัท การตลาดดิจิทัล จำกัด
        Job('30000001', 'Digital Marketing Manager', 'วางแผนและดำเนินการตลาดออนไลน์', '34567890', future_date, 'งานปกติ', 'เปิด'),
        Job('30000002', 'สหกิจศึกษา - Social Media', 'เรียนรู้การบริหาร Social Media', '34567890', future_date, 'สหกิจศึกษา', 'เปิด'),
        Job('30000003', 'SEO Specialist', 'เพิ่มประสิทธิภาพการค้นหาในเว็บไซต์', '34567890', future_date, 'งานปกติ', 'เปิด'),
        Job('30000004', 'Content Creator', 'สร้างเนื้อหาสำหรับแพลตฟอร์มต่างๆ', '34567890', future_date, 'งานปกติ', 'เปิด'),
    ]
    
    for job in jobs:
        db.session.add(job)
    
    # Seed users for authentication
    users = [
        # Admin user
        User('admin', 'admin@system.com', 'admin123', 'admin'),
        
        # Company users
        User('tech_hr', 'hr@tech-company.co.th', 'tech123', 'company', company_id='12345678'),
        User('finance_hr', 'recruit@finance-corp.co.th', 'finance123', 'company', company_id='23456789'),
        User('marketing_hr', 'jobs@digital-marketing.co.th', 'marketing123', 'company', company_id='34567890'),
        
        # Regular users (candidates)
        User('somchai', 'somchai@email.com', 'pass123', 'user', candidate_id='11111111'),
        User('supaporn', 'supaporn@email.com', 'pass123', 'user', candidate_id='22222222'),
        User('wichai', 'wichai@email.com', 'pass123', 'user', candidate_id='33333333'),
        User('malee', 'malee@email.com', 'pass123', 'user', candidate_id='44444444'),
        User('thana', 'thana@email.com', 'pass123', 'user', candidate_id='55555555'),
    ]
    
    for user in users:
        db.session.add(user)
    
    # Commit all data
    db.session.commit()
    
    print("✅ Sample data created successfully!")
    print(f"✅ Created {len(companies)} companies")
    print(f"✅ Created {len(candidates)} candidates")
    print(f"✅ Created {len(jobs)} jobs")
    print(f"✅ Created {len(users)} users")
    print("\n📋 Login credentials:")
    print("Admin: admin / admin123")
    print("Company (Tech): tech_hr / tech123")
    print("User (Somchai): somchai / pass123")