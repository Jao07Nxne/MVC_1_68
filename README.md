# 🚀 CS Job Fair - ระบบรับสมัครงาน (Job Recruitment System)

## 📋 รายละเอียดโปรเจกต์

ระบบรับสมัครงานออนไลน์ที่พัฒนาด้วย **Python Flask** ตามแนวทาง **MVC Architecture** รองรับการจัดการตำแหน่งงานและสหกิจศึกษาสำหรับบริษัทและผู้สมัครงาน พร้อม Modern UI/UX ด้วย Bootstrap 5

**🏷️ เวอร์ชัน:** 1.1 
**📊 สถานะ:** Production Ready  
**🗂️ Repository:** https://github.com/Jao07Nxne/MVC_1_68

---

## ✨ ฟีเจอร์หลัก (Version 1.1)

### 👥 ระบบผู้ใช้งาน (Multi-Role Authentication)
- **🔴 Admin** - จัดการระบบทั้งหมด, รายงานสถิติ, การตั้งค่า
- **🔵 Company** - โพสต์งาน, จัดการใบสมัคร, อัพเดทสถานะ
- **🟢 User/Candidate** - สมัครงาน, ติดตามสถานะ, จัดการโปรไฟล์

### 💼 การจัดการตำแหน่งงาน
- โพสต์ตำแหน่ง**งานปกติ** (สำหรับผู้จบการศึกษา)
- โพสต์ตำแหน่ง**สหกิจศึกษา** (สำหรับนักศึกษา)
- กรองและค้นหาตามประเภทงาน
- การแสดงวันคงเหลือแบบ Real-time
- ระบบสถานะการเปิด/ปิดรับสมัครอัตโนมัติ

### 📝 ระบบสมัครงาน
- สมัครงานออนไลน์ตามคุณสมบัติ (กำลังศึกษา/จบแล้ว)
- ติดตามสถานะใบสมัคร (รอดำเนินการ/อนุมัติ/ปฏิเสธ)
- ประวัติการสมัครงานแบบครบถ้วน
- Dashboard แยกตาม Role พร้อมสถิติ

### 👤 ระบบโปรไฟล์
- แสดงข้อมูลโปรไฟล์ผู้ใช้
- แก้ไขข้อมูลส่วนตัว (ชื่อ, นามสกุล, อีเมล, สถานะ)
- เมนูโปรไฟล์ใน Navbar

### 📊 ระบบรายงาน (Admin Only)
- สถิติตำแหน่งงานและใบสมัคร
- การวิเคราะห์ข้อมูลผู้ใช้
- รายงานบริษัทและผู้สมัครยอดนิยม

### 🎨 Modern UI/UX
- **Orange Theme** (#E35205) เป็นสีหลัก
- **Bootstrap 5** พร้อม Custom CSS
- **Responsive Design** รองรับทุกอุปกรณ์
- **Thai Typography** (Kanit + Sarabun fonts)

---

## 🏗️ สถาปัตยกรรม (MVC Architecture)

```
📦 MVC_1_68/
├── 📂 app/
│   ├── 📂 models/           # 🗂️ MODEL: Data & Business Logic
│   │   ├── company.py       # โมเดลบริษัท
│   │   ├── job.py          # โมเดลตำแหน่งงาน  
│   │   ├── candidate.py    # โมเดลผู้สมัคร
│   │   ├── user.py         # โมเดลผู้ใช้ (Authentication)
│   │   ├── application.py  # โมเดลใบสมัคร
│   │   └── seed_data.py    # ข้อมูลตัวอย่าง
│   │
│   ├── 📂 controllers/      # 🎮 CONTROLLER: Request/Response
│   │   ├── main_controller.py    # หน้าหลัก, Dashboard, โปรไฟล์
│   │   ├── auth_controller.py    # ล็อกอิน, ลงทะเบียน
│   │   └── job_controller.py     # งาน, ใบสมัคร
│   │
│   └── 📂 templates/        # 🎨 VIEW: User Interface
│       ├── base.html        # Layout หลัก
│       ├── index.html       # หน้าแรก
│       ├── profile.html     # โปรไฟล์
│       ├── edit_profile.html # แก้ไขโปรไฟล์
│       ├── *_dashboard.html # Dashboard แต่ละ Role
│       ├── 📂 auth/         # หน้า Authentication
│       └── 📂 jobs/         # หน้างานและใบสมัคร
│
├── 📄 app.py               # Entry Point
├── 📄 extensions.py        # Flask Extensions
├── 📄 requirements.txt     # Dependencies
├── 📄 .gitignore          # Git Ignore Rules
└── 📄 README.md           # คู่มือโปรเจกต์
```

---

## 🛠️ เทคโนโลยีที่ใช้

### Backend
- **Python 3.8+**
- **Flask 2.3.3** - Web Framework
- **SQLAlchemy** - ORM Database
- **Flask-Login** - User Session Management
- **Werkzeug** - Password Hashing

### Frontend  
- **Bootstrap 5** - CSS Framework
- **Font Awesome 6** - Icons
- **Google Fonts** - Kanit + Sarabun
- **Vanilla JavaScript** - Interactions

### Database
- **SQLite** - สำหรับ Development
- **PostgreSQL/MySQL** - พร้อมสำหรับ Production

---

## 🚀 วิธีการติดตั้งและรัน

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Jao07Nxne/MVC_1_68.git
cd MVC_1_68
```

### 2️⃣ สร้าง Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate
```

### 3️⃣ ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ รันระบบ
```bash
python app.py
```

### 5️⃣ เข้าใช้งานระบบ
เปิด Browser ไปที่: **http://127.0.0.1:5000**

---

## 👤 บัญชีทดสอบ (Default Accounts)

| บทบาท | Username | Password | คำอธิบาย |
|--------|----------|----------|----------|
| **Admin** | `admin` | `admin123` | ผู้ดูแลระบบ |
| **Company** | `tech_hr` | `tech123` | บริษัท เทคโนโลยี |
| **Company** | `finance_hr` | `finance123` | บริษัท การเงิน |
| **User** | `somchai` | `pass123` | ผู้สมัครงาน (กำลังศึกษา) |
| **User** | `supaporn` | `pass123` | ผู้สมัครงาน (จบแล้ว) |

---

## 📋 Routes หลัก

### 🔐 Authentication (`/auth/*`)
- `/auth/login` - เข้าสู่ระบบ
- `/auth/logout` - ออกจากระบบ
- `/auth/register` - สมัครสมาชิก

### 🏠 Main Routes (`/`)
- `/` - หน้าแรกแสดงตำแหน่งงาน
- `/dashboard` - Dashboard (แยกตาม Role)
- `/profile` - โปรไฟล์ผู้ใช้
- `/profile/edit` - แก้ไขโปรไฟล์
- `/admin/reports` - รายงานสถิติ (Admin)
- `/admin/settings` - ตั้งค่าระบบ (Admin)

### 💼 Job Routes (`/jobs/*`)
- `/jobs/` - รายการตำแหน่งงาน
- `/jobs/<job_id>` - รายละเอียดงาน
- `/jobs/<job_id>/apply` - สมัครงาน
- `/jobs/my_applications` - ใบสมัครของฉัน
- `/jobs/company_applications` - ใบสมัครบริษัท

---

## 🗂️ ฐานข้อมูล (Database Schema)

### 📊 Entity Relationship
```
👥 User (1) -----> (0,1) 👤 Candidate
👥 User (1) -----> (0,1) 🏢 Company  
🏢 Company (1) --> (0,*) 💼 Job
👤 Candidate (1) -> (0,*) 📝 Application
💼 Job (1) -------> (0,*) 📝 Application
```

### 🏷️ สถานะ (Status Values)
- **Candidate Status**: `กำลังศึกษา`, `จบแล้ว`
- **Job Type**: `งานปกติ`, `สหกิจศึกษา`
- **Job Status**: `เปิด`, `ปิด`
- **Application Status**: `รอดำเนินการ`, `อนุมัติ`, `ปฏิเสธ`

---

## 📞 ติดต่อ

**Developer:** [Jao07Nxne](https://github.com/Jao07Nxne)  
**Project Link:** [https://github.com/Jao07Nxne/MVC_1_68](https://github.com/Jao07Nxne/MVC_1_68)

---


