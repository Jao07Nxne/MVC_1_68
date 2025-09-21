# Views Layer - Template Rendering Functions
# 
# ในโปรเจกต์นี้ View Layer แบ่งเป็น 2 ส่วน:
# 1. Controllers - จัดการ Business Logic และเรียก Templates
# 2. Templates - HTML Files สำหรับแสดงผล (อยู่ใน app/templates/)
#
# โฟลเดอร์นี้สามารถใช้สำหรับ:
# - View Helper Functions
# - Template Filters
# - Custom Template Functions

def format_thai_date(date):
    """แปลงวันที่เป็นรูปแบบไทย"""
    thai_months = [
        'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
        'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
    ]
    
    if date:
        return f"{date.day} {thai_months[date.month - 1]} {date.year + 543}"
    return ""

def format_job_status(status):
    """แปลงสถานะงานเป็นสีและไอคอน"""
    status_config = {
        'เปิด': {'color': 'success', 'icon': 'fa-check-circle'},
        'ปิด': {'color': 'danger', 'icon': 'fa-times-circle'},
        'รอ': {'color': 'warning', 'icon': 'fa-clock'}
    }
    
    return status_config.get(status, {'color': 'secondary', 'icon': 'fa-question'})

def calculate_days_remaining(deadline):
    """คำนวณจำนวนวันที่เหลือ"""
    from datetime import datetime
    
    if not deadline:
        return None
        
    today = datetime.now().date()
    delta = deadline - today
    
    return delta.days if delta.days >= 0 else 0