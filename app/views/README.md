"""
📋 MVC Architecture ในโปรเจกต์นี้

┌─ MVC_1_68/
├─ app/
│  ├─ 📂 models/          ← MODEL: ข้อมูลและ Business Logic
│  │  ├─ company.py       (บริษัท)
│  │  ├─ job.py          (ตำแหน่งงาน)
│  │  ├─ candidate.py    (ผู้สมัคร)
│  │  ├─ user.py         (ผู้ใช้)
│  │  └─ application.py  (ใบสมัคร)
│  │
│  ├─ 📂 controllers/     ← CONTROLLER: จัดการ Request/Response
│  │  ├─ main_controller.py    (หน้าหลัก)
│  │  ├─ auth_controller.py    (ล็อกอิน/ลงทะเบียน)
│  │  └─ job_controller.py     (จัดการงาน)
│  │
│  ├─ 📂 templates/       ← VIEW: HTML Templates สำหรับแสดงผล
│  │  ├─ base.html        (Template หลัก)
│  │  ├─ index.html       (หน้าแรก)
│  │  ├─ auth/           (หน้า Login/Register)
│  │  └─ jobs/           (หน้าเกี่ยวกับงาน)
│  │
│  ├─ 📂 views/          ← VIEW HELPERS: ฟังก์ชันช่วยเหลือ Templates
│  │  ├─ helpers.py       (ฟังก์ชันช่วยเหลือ)
│  │  └─ __init__.py
│  │
│  └─ 📂 static/         ← ASSETS: CSS, JS, Images
│     ├─ css/
│     ├─ js/
│     └─ images/

🔄 การทำงานของ MVC:
1. User ส่ง Request → CONTROLLER
2. CONTROLLER เรียกใช้ → MODEL (ดึงข้อมูล)  
3. CONTROLLER ส่งข้อมูลไป → VIEW (Template)
4. VIEW แสดงผล HTML กลับไปที่ User

💡 ใน Flask:
- Views = Templates (HTML Files)
- Controllers = Route Functions
- Models = Database Models
"""